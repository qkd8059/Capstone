import base64
import datetime as dt
import hashlib
import os
import re
import secrets
import threading

from flask import Flask, Response, abort, jsonify, redirect, request

from app.portfolio import master
from app.database_main import Database as PortfolioData

from database import DB

# TODO change to domain url once we can
URL = 'http://zhangfinance.rocks'

app = Flask(__name__)

def valid_request(req, expected_fields, is_json=False):
    if is_json:
        if not req.is_json:
            return False
        return set(expected_fields).issubset(req.get_json().keys())
    else:
        return set(expected_fields).issubset(req.form.keys())

@app.route('/', methods=['GET'])
def hello():
    return 'This is the backend'

@app.route('/sign-up', methods=['POST'])
def sign_up():
    if not valid_request(request, ['first_name', 'last_name', 'email', 'password']):
        return abort(400)
    
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']

    salt = secrets.token_bytes(16)
    master_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)

    DB.create_user(
        first_name,
        last_name,
        email,
        base64.b64encode(salt).decode('utf-8'),
        base64.b64encode(master_key).decode('utf-8')
    )

    return redirect(f'{URL}/sign-in/sign-in.html', 303)

@app.route('/sign-in', methods=['POST'])
def sign_in():
    if not valid_request(request, ['email', 'password']):
        return abort(400)

    email = request.form['email']
    password = request.form['password']
    remember = 'remember' in request.form.keys()

    user = DB.get_user(email)

    if user is not None:
        salt = base64.b64decode(user['salt'].encode('utf-8'))
        master_key = base64.b64decode(user['master_key'].encode('utf-8'))

        if master_key == hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000):
            max_age, expiration = None, None
            last_used = dt.datetime.now()
            if remember:
                max_age = dt.timedelta(days=365)
                expiration = last_used + max_age

            success = False
            while not success:
                session_id = secrets.token_hex(64)
                success = DB.create_session(email, session_id, expiration, last_used)

            resp = redirect(f'{URL}/dashboard/dashboard.html', 303)
            resp.set_cookie('session_id', session_id, max_age=max_age)
            return resp
    
    return redirect(f'{URL}/sign-in/sign-in-failed.html', 303)

@app.route('/sign-out', methods=['POST'])
def sign_out():
    if not valid_request(request, ['cookie'], True):
        return 'invalid request', 400

    cookies = request.get_json()['cookie']

    try:
        session_id = re.search(r'session_id=(\w+)', cookies).groups()[0]
        DB.remove_session(session_id)
    except:
        pass
    finally:
        resp = redirect(f'{URL}/sign-in/sign-in.html', 303)
        resp.set_cookie('session_id', '', expires=dt.datetime(year=1971, month=1, day=1))
        return resp

@app.route('/check-session-id', methods=['POST'])
def check_session_id():
    if not valid_request(request, ['cookie'], True):
        return 'invalid request', 400

    try:
        cookies = request.get_json()['cookie']
        session_id = re.search(r'session_id=(\w+)', cookies).groups()[0]

        if DB.get_session(session_id) is not None:
            return 'logged in', 200
    except:
        pass

    return 'logged out', 200

@app.route('/create-portfolio', methods=['POST'])
def create_portfolio():
    req_fields = [
        'primary_objective',
        'target_return',
        'start_date',
        'end_date',
        'initial_contribution',
        'rebalance_freq',
        'risk_appetite',
        'portfolio_name',
        'session_id'
    ]
    if not valid_request(request, req_fields):
        return abort(400)

    if (session := DB.get_session(request.form['session_id'])) is None:
        return abort(400)

    # primary_objective = request.form['primary_objective']
    target_return = float(request.form['target_return'])
    start_date = dt.datetime.strptime(request.form['start_date'], r'%Y-%m-%d')
    end_date = dt.datetime.strptime(request.form['end_date'], r'%Y-%m-%d')
    initial_contribution = float(request.form['initial_contribution'])
    rebalance_freq = int(request.form['rebalance_freq'])
    risk_appetite = float(request.form['risk_appetite'])
    portfolio_name = request.form['portfolio_name']

    # secondary_objective = 'secondary_objective' in request.form and request.form['secondary_objective']
    cardinality_constraint = 10
    if 'cardinality_constraint' in request.form:
        try:
            cardinality_constraint = int(request.form['cardinality_constraint'])
        except ValueError:
            pass

    portfolio_description = ''
    if 'portfolio_description' in request.form:
        portfolio_description = request.form['portfolio_description']

    # esg_impact = 'esg_impact' in request.form
    # primary_portfolio = 'primary_portfolio' in request.form
    # model_backtesting = 'model_backtesting' in request.form


    time_horizon = max((end_date - start_date).days // 7, 250)

    args = [
        target_return,
        time_horizon,
        initial_contribution,
        cardinality_constraint,
        rebalance_freq,
        risk_appetite
    ]

    '''
    ticker_label
    weight
    annual_return
    annual_std
    sharpe_ratio
    normalized_dates
    normalized_ret
    normalized_SPY_ret
    normalized_6040_ret
    annual_return_SPY
    annual_std_SPY
    sharpe_ratio_SPY
    annual_return_6040
    annual_std_6040
    sharpe_ratio_6040
    '''

    def generate_portfolio():
        print('Generating portfolio...')
        portfolio_vars = list(master(*args))
        # portfolio_vars = list(master(0.2, 300, 10000, 10, 104, 0.2))
        portfolio = [portfolio_name, portfolio_description] + args + portfolio_vars

        DB.add_portfolio(session['email'], portfolio)
        print('Portfolio created successfully!')

    threading.Thread(target=generate_portfolio, daemon=True).start()

    return redirect(f'{URL}/dashboard/dashboard.html', 303)

@app.route('/dashboard-line-chart', methods=['POST'])
def dashboard_line_chart():
    if not valid_request(request, ['portfolio', 'session_id'], is_json=True):
        return abort(400)

    if (session := DB.get_session(request.get_json()['session_id'])) is None:
        return abort(400)
    
    email = session['email']
    portfolio_number = request.get_json()['portfolio']

    portfolios = DB.get_user(email)['portfolios']
    portfolio_names = [pf[0] for pf in portfolios]

    portfolio = portfolios[portfolio_number]

    portfolio_name, \
    portfolio_desc, \
    target_return, \
    time_horizon, \
    initial_contribution, \
    cardinality_constraint, \
    rebalance_freq, \
    risk_appetite, \
    ticker_label, \
    weight, \
    annual_return, \
    annual_std, \
    sharpe_ratio, \
    normalized_dates, \
    normalized_ret, \
    normalized_SPY_ret, \
    normalized_6040_ret, \
    annual_return_SPY, \
    annual_std_SPY, \
    sharpe_ratio_SPY, \
    annual_return_6040, \
    annual_std_6040, \
    sharpe_ratio_6040 = portfolio

    # somehow generate a dict/JSON of data to make the line graph
    ticker_prices=[]
    for i in ticker_label:
        ticker_prices.append(PortfolioData.get_one_price(i))

    # or data = {}
    Projected_Performance = {
        'dates': normalized_dates,             #x
        'ret': normalized_ret,                 #y1
        'ret_spy': normalized_SPY_ret,         #y2
        'ret_6040': normalized_6040_ret        #y3
    }
    Portfolio_Composition = {
        'tickers': ticker_label,
        'weights': weight
    }
    Asset_Allocation = {
        'tickers': ticker_label,
        'weights': [round(100*w, 2) for w in weight],
        'prices': ticker_prices
    }
    Statistical_Measurement = {
        'rets': round(annual_return, 3),
        'std': round(annual_std, 3),
        'sharpe': round(sharpe_ratio, 3)
    }
    Portfolio_Menu ={
        'names': portfolio_names,
        'current': portfolio_name
    }

    data = [Projected_Performance, Portfolio_Composition, Asset_Allocation, Statistical_Measurement, Portfolio_Menu]

    resp = jsonify(data)
    resp.status_code = 200
    return resp
