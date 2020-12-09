import numpy as np
import cvxpy as cp


def mvo_cost(mu, Q, card, old_weight, old_ticker):
    """
    :param mu: n*1 vector, expected returns of n assets
    :param Q: n*n matrix, covariance matrix of n assets
    :param card: a scalar, cardinality constraint
    :param old_weight: k*1 vector, weights of k stocks in the portfolio during the previous period
    :param old_ticker: k*1 vecotr, indices of k stocks in the portfolio during the previous period
    :return: norm_weight (the portfolio weight), ticker_index (the indices of selected stock)
    """
    # Define the variables: w-weight, y-auxiliary variable for eliminating absolute values of transaction constraint
    w = cp.Variable(len(mu))
    y = cp.Variable(len(mu))

    # Create the weight array of the previous time period
    w_old = np.zeros(len(mu))
    w_old[old_ticker] = old_weight

    # Create objective function: Minimize w^T*Q*w - gamma*mu^T*w
    p = Q
    p = p.T @ p
    lamb = 0.001
    q = lamb * mu

    # set the upper limit of the weight (w_i) to be 50% to avoid over-concentration
    up = 0.5
    # Create inequality constraint matrix: 0 <= w_i <= 0.5
    # Disallow short selling
    G = -np.identity(len(mu))
    j = np.identity(len(mu))
    G = np.append(G, j, axis=0)
    h = np.zeros(len(mu)).reshape((len(mu)))
    i = (np.ones(len(mu)) * up).reshape((len(mu)))
    h = np.append(h, i, axis=0)

    # Create equality constraint matrix: sum(w_i) = 1
    A = np.array([1.0] * len(mu)).reshape((1, len(mu)))
    b = np.array([1.0])

    # Create the transaction cost constraint: w_i - w_i_old <= y_i
    # w_i_old - w_i <= y_i, sum(c_i*y_i) <= T
    # Define cost per transaction
    cost = 0.01
    # Define total cost
    total_cost = 0.5 + lookback*0.01   #longer rebalancing period will tolerate more weight shift
    c = np.identity(len(mu)) * cost
    T = np.array([total_cost])

    # Use cvxpy default optimizer
    obj = cp.Minimize(cp.quad_form(w, p) - q.T @ w)
    constraints = [G @ w <= h,
                   A @ w == b,
                   w - w_old <= y,
                   c @ y <= T]
    prob = cp.Problem(obj, constraints)
    prob.solve()
    weight = w.value

    # Return the indices of the selected stocks
    ticker_index = np.asarray(weight).argsort()[-card:]

    # Return the weight based on the cardinality and normalize the weight to avoid extremely small weights (e.g. 10^-10)
    weight.sort()
    weight_opt = weight[-card:]
    norm_weight = [float(i) / np.sum(weight_opt) for i in weight_opt]
    return norm_weight, ticker_index
