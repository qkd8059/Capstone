import numpy as np
from scipy.optimize import minimize


def risk_parity_cost(mu, Q, card, old_weight, old_ticker):
    """
    :param mu: n*1 vector, expected returns of n assets
    :param Q: n*n matrix, covariance matrix of n assets
    :param card: a scalar, cardinality constraint
    :param old_weight: k*1 vector, weights of k stocks in the portfolio during the previous period
    :param old_ticker: k*1 vecotr, indices of k stocks in the portfolio during the previous period
    :return: norm_weight (the portfolio weight), ticker_index (the indices of selected stock)
    """
    def _allocation_risk(weights, covariances):
        # We calculate the risk of the weights distribution
        portfolio_risk = np.sqrt((weights * covariances * weights.T))[0, 0]
        # It returns the risk of the weights distribution
        return portfolio_risk

    def _assets_risk_contribution_to_allocation_risk(weights, covariances):
        # We calculate the risk of the weights distribution
        portfolio_risk = _allocation_risk(weights[0:num_assets], covariances)
        # We calculate the contribution of each asset to the risk of the weights distribution
        assets_risk_contribution = np.multiply(weights[0:num_assets].T, covariances * weights[0:num_assets].T) \
        / portfolio_risk
        # It returns the contribution of each asset to the risk of the weights distribution
        return assets_risk_contribution

    def _risk_budget_objective_error(weights, args):
        # The covariance matrix occupies the first position in the variable
        covariances = args[0]
        # The desired contribution of each asset to the portfolio risk occupies the
        # second position
        assets_risk_budget = args[1]
        # We convert the weights to a matrix
        weights = np.matrix(weights[0:num_assets])
        # We calculate the risk of the weights distribution
        portfolio_risk = _allocation_risk(weights, covariances)
        # We calculate the contribution of each asset to the risk of the weights
        # distribution
        assets_risk_contribution = _assets_risk_contribution_to_allocation_risk(weights, covariances)
        # We calculate the desired contribution of each asset to the risk of the
        # weights distribution
        assets_risk_target = np.asmatrix(np.multiply(portfolio_risk, assets_risk_budget))
        # Error between the desired contribution and the calculated contribution of
        # each asset
        error = sum(np.square(assets_risk_contribution - assets_risk_target.T))[0, 0]
        # It returns the calculated error
        return error

    # equal risk distribution
    assets_risk_budget = 1/card

    # Restrictions to consider in the optimisation: only long positions whose
    # sum equals 100%
    def check_sum(weights):
        return np.sum(weights[0:num_assets]) - 1

    # Create the transaction cost constraint: x_i - x_i_old <= y_i
    # x_i_old - x_i <= y_i, sum(c_i*y_i) <= T
    # Define cost per transaction
    def cost_pos(weights,old_weight=old_weight, old_ticker=old_ticker):
        w_old = np.zeros(len(mu))
        w_old[old_ticker] = old_weight
        return w_old - weights[0:num_assets] + weights[num_assets:]
    def cost_neg (weights, old_weight=old_weight, old_ticker=old_ticker):
        w_old = np.zeros(len(mu))
        w_old[old_ticker] = old_weight
        return - w_old + weights[0:num_assets] + weights[num_assets:]
    def T_cost (weights, cost=0.01, total_cost=100):
        return np.hstack((np.zeros(num_assets),-np.ones(num_assets)*cost))+total_cost
    cons = ({'type':'eq','fun':check_sum},
            {'type':'ineq','fun':cost_pos},
            {'type':'ineq','fun':cost_neg},
            {'type':'ineq','fun':T_cost})

    # Initial weights: equally weighted
    num_assets = len(mu)
    up = 0.5
    bds = [None] * (2*num_assets)
    for i in range (2*num_assets):
        if i < num_assets:
            bds[i] = (0,up)
        else:
            bds[i] = (None, None)

    initial_weights = num_assets * [1./num_assets,]+list(np.zeros(num_assets))
    # set the bounds for the weight
    # Optimisation process in scipy
    TOLERANCE = 1e-10
    optimize_result = minimize(fun=_risk_budget_objective_error,
        x0=initial_weights,
        args=[Q, assets_risk_budget],
        # method='SLSQP',
        method = 'CG',
        bounds = bds,
        constraints=cons,
        tol=TOLERANCE,
        options={'disp': False})
    # Recover the weights from the optimised object
    weights = optimize_result.x[0:num_assets]
    # Return the indices of the selected stocks
    ticker_index = np.argsort(weights)[-card:]
    # Return the weight based on the cardinality and normalize the weight to avoid extremely small weights (e.g. 10^-10)
    weight_opt = weights[np.argsort(weights)[-card:]]
    norm_weight = [float(i)/sum(weight_opt) for i in weight_opt]
    return norm_weight, ticker_index