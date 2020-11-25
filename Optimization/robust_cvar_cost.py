import numpy as np
from scipy.optimize import linprog
from matrix_helper import *


# Robust CVaR with Transaction Cost
def robust_cvar_cost(mu,Q, card, price_table, date, old_weight, old_ticker):
    """
    :param mu: n*1 vector, expected returns of n assets
    :param Q: n*n matrix, covariance matrix of n assets
    :param card: a scalar, cardinality constraint
    :param price_table: n*T matrix, prices of n assets over T time periods
    :param date: a string as yyyy-mm-dd, current date when rebalancing
    :param old_weight: k*1 vector, weights of k stocks in the portfolio during the previous period
    :param old_ticker: k*1 vecotr, indices of k stocks in the portfolio during the previous period
    :return: norm_weight (the portfolio weight), ticker_index (the indices of selected stock)
    """
    # Define parameters used for Monte Carlo simulation
    ## the number of simulated asset price paths
    num_paths = 1000
    ## get current prices of the current date
    current_prices = price_table[date]
    ## the time length of simulation in the unit of estimation of mu and Q. Here T represents rebalancing every 8 weeks
    T = 4
    ## the number of time steps to take in the simulation
    N = 1
    ## confident level for the VaR
    alpha = 0.95

    # Create the weight array of the previous time period
    w_old = np.zeros(len(mu))
    w_old[old_ticker] = old_weight

    # Create the weight array of the previous time period
    w_old = np.zeros(len(mu))
    w_old[old_ticker] = old_weight
    num_assets = len(mu)

    # Monte Carlo simulation to obtain sample return of each path for each asset
    rho = get_correlation_from_covariance_matrix(Q)
    L = np.linalg.cholesky(rho)
    dt = T / N
    stock_price = np.ones((num_assets, num_paths))
    for i in range(num_assets):
        for j in range(num_paths):
            stock_price[i][j] = current_prices[i]
    for j in range(num_paths):
        for i in range(N):
            ran = np.random.normal(0, 1, num_assets)
            x = np.matmul(L, ran)
            for k in range(num_assets):
                stock_price[k][j] = stock_price[k][j] * np.exp( (mu[k] - 0.5 * Q[k][k]) * dt + ((Q[k][k] * dt)**0.5) * x[k])
    returns_sample = np.ones((num_assets, num_paths))
    for i in range(num_assets):
        for j in range(num_paths):
            returns_sample[i][j] = stock_price[i][j] / current_prices[i] - 1

    # construct a box uncertainty set
    theta = np.diag(np.diag(Q/num_paths))
    sqrt_theta = np.sqrt(theta)
    # set a 90% confidence interval for the true mu
    ep = 1.645
    delta = ep*np.diag(sqrt_theta)

    # Create objective function: min gamma+1/[(1-alpha)S]*sum z_s - lambda*mu^T*x + lambda*delta*x
    lamb = 0.001
    f1 = -lamb*mu+lamb*delta
    f2 = (1/((1-alpha)*num_paths))*np.ones(num_paths)
    f3 = 1
    f4 = np.zeros(num_assets)
    f = np.hstack((f1,f2,f3,f4))


    # Create inequality constraint matrix: z_s >= 0, z_s >= -r_s^T*x - gamma, 0 <= x_i <= 0.5
    # Create the transaction cost constraint: x_i - x_i_old <= y_i
    # x_i_old - x_i <= y_i, sum(c_i*y_i) <= T
    # Define cost per transaction
    cost = 0.01
    # Define total cost
    total_cost = 100
    rs = returns_sample.T
    z = -np.identity(num_paths)
    gamma = -np.ones(num_paths).reshape(num_paths,1)
    cost0 = np.zeros((num_paths,num_assets))
    cost_pos = np.hstack((np.identity(num_assets),np.zeros((num_assets,num_paths+1)),-np.identity(num_assets)))
    cost_neg = np.hstack((-np.identity(num_assets),np.zeros((num_assets,num_paths+1)),-np.identity(num_assets)))
    cost_total = np.hstack((np.zeros(num_assets+num_paths+1),np.ones(num_assets)*cost))
    G = np.hstack((-rs, z, gamma,cost0))
    G = np.vstack((G,cost_pos,cost_neg,cost_total))
    h = np.hstack((np.zeros(num_paths),w_old,-w_old,total_cost))
    up = 0.5
    bds = [None] * (2 * num_assets + num_paths + 1)
    for i in range(2 * num_assets + num_paths + 1):
        if i < num_assets:
            bds[i] = (0, up)
        else:
            bds[i] = (None, None)

    # Create equality matrix: 1^T*x = 1
    Aeq = np.hstack((np.ones(num_assets),np.zeros(num_paths+1+num_assets)))
    beq = np.array([1.0])

    # Use linprog optimizer in scipy to optimize
    result = linprog(f, A_ub = G, b_ub = h, A_eq = Aeq.reshape(1,2*num_assets+num_paths+1), b_eq = beq, bounds = bds)
    weight = result.x
    weight = weight[0:num_assets]
    # Return the indices of the selected stocks
    ticker_index = np.argsort(weight)[-card:]
    # Return the weight based on the cardinality and normalize the weight to avoid extremely small weights (e.g. 10^-10)
    weight_opt = weight[np.argsort(weight)[-card:]]
    norm_weight = [float(i)/np.sum(weight_opt) for i in weight_opt]
    return norm_weight, ticker_index
