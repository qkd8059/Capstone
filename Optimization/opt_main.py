from mvo import *
from mvo_cost import *
from cvar import *
from cvar_cost import *
from robust_cvar import *
from robust_cvar_cost import *
from max_sharpe import *
from max_sharpe_cost import *
from risk_parity import *
from risk_parity_cost import *

class optimization (object):
    def cardinality (principal):
        if principal <= 10000:
            card = 10
        elif principal > 10000 and principal <= 100000:
            card = 15
        else: card = 20
        return card
            def choose_model (regime_flag):
                if regime_flag == 0:
                    model_flag = 1
                        cost_flag = 1
        else:
            model_flag = 2
                cost_flag = 1
        return model_flag, cost_flag
    def get_weight (card, price_table, date, old_weight, old_ticker, model_flag, cost_flag):
        opt_model = [[mvo,mvo_cost],[cvar,cvar_cost],[robust_cvar,robust_cvar_cost],
                     [max_sharpe, max_sharpe_cost],[risk_parity, risk_parity_cost]]
        if model_flag == 1 or model_flag == 2:
            if cost_flag == 0:
                weight, ticker_index = opt_model[model_flag][cost_flag](mu,Q,card,price_table,date)
            else:
                weight, ticker_index = opt_model[model_flag][cost_flag](mu,Q, card, price_table, date, old_weight, old_ticker)
        else:
            if cost_flag == 0:
                weight, ticker_index = opt_model[model_flag][cost_flag](mu,Q,card)
            else:
                weight, ticker_index = opt_model[model_flag][cost_flag](mu,Q, card, old_weight, old_ticker)
        return weight, ticker_index

card = optimization.cardinality(20000)
price_table = df
date = ['2010-10-22']
init_old_weight = np.zeros(card)
init_old_ticker = np.arange(card)
m_f, c_f = optimization.choose_model(0)
w, t = optimization.get_weight(card,price_table,date,init_old_weight, init_old_ticker, m_f, c_f)
print(w,t)

