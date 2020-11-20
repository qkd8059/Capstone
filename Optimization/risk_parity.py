import numpy as np
from scipy.optimize import minimize


# Risk Parity Optimization
def risk_parity(mu,Q,card):
    """
    :param mu: n*1 vector, expected returns of n assets
    :param Q: n*n matrix, covariance matrix of n assets
    :param card: a scalar, cardinality constraint
    :return: norm_weight (the portfolio weight), ticker_index (the indices of selected stock)
    """
    def _allocation_risk(weights, covariances):
        # We calculate the risk of the weights distribution
        portfolio_risk = np.sqrt((weights * covariances * weights.T))[0, 0]
        # It returns the risk of the weights distribution
        return portfolio_risk
    def _assets_risk_contribution_to_allocation_risk(weights, covariances):
        # We calculate the risk of the weights distribution
        portfolio_risk = _allocation_risk(weights, covariances)
        # We calculate the contribution of each asset to the risk of the weights distribution
        assets_risk_contribution = np.multiply(weights.T, covariances * weights.T) \
        / portfolio_risk
        # It returns the contribution of each asset to the risk of the weights distribution
        return assets_risk_contribution
    def _risk_budget_objective_error(weights, args):
        # The covariance matrix occupies the first position in the variable
        covariances = args[0]
        # The desired contribution of each asset to the portfolio risk occupies the second position
        assets_risk_budget = args[1]
        # We convert the weights to a matrix
        weights = np.matrix(weights)
        # We calculate the risk of the weights distribution
        portfolio_risk = _allocation_risk(weights, covariances)
        # We calculate the contribution of each asset to the risk of the weights distribution
        assets_risk_contribution = _assets_risk_contribution_to_allocation_risk(weights, covariances)
        # We calculate the desired contribution of each asset to the risk of the weights distribution
        assets_risk_target = np.asmatrix(np.multiply(portfolio_risk, assets_risk_budget))
        # Error between the desired contribution and the calculated contribution of each asset
        error = sum(np.square(assets_risk_contribution - assets_risk_target.T))[0, 0]
        # It returns the calculated error
        return error
    # equal risk distribution
    assets_risk_budget = 1/card
    # Restrictions to consider in the optimisation: only long positions whose
    # sum equals 100%
    # check allocation sums to 1
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1.0},
                  {'type': 'ineq', 'fun': lambda x: x})

    # Initial weights: equally weighted
    num_assets = len(mu)
    initial_weights = num_assets * [1./num_assets,]
    # set the bounds for the weight
    up = 0.5
    bds = tuple((0,up) for x in range(num_assets))

    # Use sequential least square quadratic programming in scipy to optimize
    TOLERANCE = 1e-10
    optimize_result = minimize(fun=_risk_budget_objective_error,
        x0=initial_weights,
        args=[Q, assets_risk_budget],
        method='SLSQP',
        # method='CG',
        bounds = bds,
        constraints=constraints,
        tol=TOLERANCE,
        options={'disp': False})
    # Recover the weights from the optimised object
    weights = optimize_result.x
    # Return the indices of the selected stocks
    ticker_index = np.argsort(weights)[-card:]
    # Return the weight based on the cardinality and normalize the weight to avoid extremely small weights (e.g. 10^-10)
    weight_opt = weights[np.argsort(weights)[-card:]]
    norm_weight = [float(i)/sum(weight_opt) for i in weight_opt]
    return norm_weight, ticker_index