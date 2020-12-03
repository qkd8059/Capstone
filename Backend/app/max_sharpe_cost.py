import numpy as np
import scipy.optimize as optimize


# Maximize Sharpe Ratio with transaction cost
def max_sharpe_cost(mu, Q, card, old_weight, old_ticker):
    """
    :param mu: n*1 vector, expected returns of n assets
    :param Q: n*n matrix, covariance matrix of n assets
    :param card: a scalar, cardinality constraint
    :param old_weight: k*1 vector, weights of k stocks in the portfolio during the previous period
    :param old_ticker: k*1 vecotr, indices of k stocks in the portfolio during the previous period
    :return: norm_weight (the portfolio weight), ticker_index (the indices of selected stock)
    """
    def get_ret_vol_sr(weights):
        weights = np.array(weights)
        ret = np.sum(mu * weights)
        vol = np.sqrt(np.dot(weights.T,np.dot(Q,weights)))
        sr = ret/vol
        return np.array([ret,vol,sr])

    # minimize negative Sharpe Ratio
    def neg_sharpe(weights):
        return get_ret_vol_sr(weights[0:num_assets])[2] * -1

    # check allocation sums to 1
    def check_sum(weights):
        return np.sum(weights[0:num_assets]) - 1

    # Create the transaction cost constraint: x_i - x_i_old <= y_i
    # x_i_old - x_i <= y_i, sum(c_i*y_i) <= T
    # Define cost per transaction
    def cost_pos(weights,old_weight=old_weight, old_ticker=old_ticker):
        w_old = np.zeros(len(mu))
        w_old[old_ticker] = old_weight
        return w_old - weights[0:num_assets] + weights[num_assets:]

    def cost_neg (weights, old_weight=old_weight,old_ticker=old_ticker):
        w_old = np.zeros(len(mu))
        w_old[old_ticker] = old_weight
        return - w_old + weights[0:num_assets] + weights[num_assets:]

    def T_cost (weights, cost=0.01, total_cost=100):
        return np.hstack((np.zeros(num_assets),-np.ones(num_assets)*cost))+total_cost
    cons = ({'type':'eq','fun':check_sum},
          {'type':'ineq','fun':cost_pos},
          {'type':'ineq','fun':cost_neg},
          {'type':'ineq','fun':T_cost})
    num_assets = len(mu)

    # Create bounds for the weights: 0 <= x_i <= 0.5
    up = 0.5
    bds = [None] * (2*num_assets)
    for i in range (2*num_assets):
        if i < num_assets:
            bds[i] = (0,up)
        else:
            bds[i] = (None, None)

    # equal weight initialization and initialize the auxiliary variable y_i to be 0
    init_guess = num_assets * [1./num_assets,]+list(np.zeros(num_assets))
    # Use sequential least square quadratic programming in scipy to optimize
    opt_results = optimize.minimize(neg_sharpe, init_guess, method='SLSQP', bounds=bds, constraints=cons)
    # opt_results = optimize.minimize(neg_sharpe, init_guess, method='CG', bounds=bds, constraints=cons)
    weight = opt_results.x[0:num_assets]
    # Return the indices of the selected stocks
    ticker_index = np.argsort(weight)[-card:]
    # Return the weight based on the cardinality and normalize the weight to avoid extremely small weights (e.g. 10^-10)
    weight_opt = weight[np.argsort(weight)[-card:]]
    norm_weight = [float(i)/sum(weight_opt) for i in weight_opt]
    return norm_weight, ticker_index