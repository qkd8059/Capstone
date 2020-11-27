import numpy as np
from matrix_helper import *


def mvo(mu, Q, card):
    """
    :param mu: n*1 vector, expected returns of n assets
    :param Q: n*n matrix, covariance matrix of n assets
    :param card: a scalar, cardinality constraint
    :return: norm_weight (the portfolio weight), ticker_index (the indices of selected stock)
    """
    # Create objective function: Minimize w^T*Q*w - gamma*mu^T*w
    p = np.array(Q)
    lamb = 0.001
    q = np.array(-lamb * mu)

    # set the upper limit of the weight (w_i) to be 50% to avoid over-concentration
    up = 0.5
    # Create inequality constraint matrix: 0 <= w_i <= 0.5
    # Disallow short selling
    G = -np.identity(len(mu))
    j = np.identity(len(mu))
    G = np.append(G, j, axis=0)
    h = np.zeros(len(mu)).reshape((len(mu)), 1)
    i = (np.ones(len(mu)) * up).reshape((len(mu)), 1)
    h = np.append(h, i, axis=0)

    # Create equality constraint matrix: sum(w_i) = 1
    A = np.array([1.0] * len(mu)).reshape((1, len(mu)))
    b = np.array([1.0])

    # Use cvxopt QP optimizer
    weight = cvxopt_solve_qp(p, q, G, h, A, b)

    # Return the indices of the selected stocks
    ticker_index = np.asarray(weight).argsort()[-card:]

    # Return the weight based on the cardinality and normalize the weight to avoid extremely small weights (e.g. 10^-10)
    weight.sort()
    weight_opt = weight[-card:]
    norm_weight = [float(i) / np.sum(weight_opt) for i in weight_opt]
    return norm_weight, ticker_index
