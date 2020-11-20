import numpy as np
import scipy.optimize as optimize


# Maximize Sharpe Ratio
def max_sharpe(mu,Q,card):
    """
    :param mu: n*1 vector, expected returns of n assets
    :param Q: n*n matrix, covariance matrix of n assets
    :param card: a scalar, cardinality constraint
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
        return get_ret_vol_sr(weights)[2] * -1
    # check allocation sums to 1
    def check_sum(weights):
        return np.sum(weights) - 1
    # create constraint variable
    cons = ({'type':'eq','fun':check_sum})
    num_assets = len(mu)
    # create bounds for the weights 0<=x_i<=0.5
    up = 0.5
    bounds = tuple((0,up) for x in range(num_assets))
    # equal weight initialization
    init_guess = num_assets * [1./num_assets,]
    # Use sequential least square quadratic programming in scipy to optimize
    opt_results = optimize.minimize(neg_sharpe, init_guess, method='SLSQP', bounds=bounds, constraints=cons)
    # opt_results = optimize.minimize(neg_sharpe, init_guess, method='CG', bounds=bounds, constraints=cons)
    weight = opt_results.x
    # Return the indices of the selected stocks
    ticker_index = np.argsort(weight)[-card:]
    # Return the weight based on the cardinality and normalize the weight to avoid extremely small weights (e.g. 10^-10)
    weight_opt = weight[np.argsort(weight)[-card:]]
    norm_weight = [float(i)/sum(weight_opt) for i in weight_opt]
    return norm_weight, ticker_index