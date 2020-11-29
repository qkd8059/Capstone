## Black-litterman Model
import numpy as np
from numpy.linalg import inv
from mvo import *
def black_litterman (mu,Q,card):
    """
    :param mu: n*1 vector, expected returns of n assets
    :param Q: n*n matrix, covariance matrix of n assets
    :param card: a scalar, cardinality constraint
    :return: norm_weight (the portfolio weight), ticker_index (the indices of selected stock)
    """
    def implied_returns(delta,sigma,w):
        ir = delta *sigma.dot(w).squeeze()
        return ir
    def proportional_prior(sigma,tau,p):
        helit_omega=p.dot(tau*sigma).dot(p.T)
        return np.diag(np.diag(helit_omega))
    def bl(w_prior,sigma_prior,p,q,omega=None,delta=2.5,tau=.02):
        if omega is None:
            omega = proportional_prior(sigma_prior,tau,p)
        N = len(w_prior)
        K = len(q)
        pi = implied_returns(delta,sigma_prior,w_prior)
        sigma_prior_scaled = tau*sigma_prior
        mu_bl = pi+sigma_prior_scaled.dot(p.T).dot(inv(p.dot(sigma_prior_scaled).dot(p.T)+omega).dot(q-p.dot(pi)))
        sigma_bl = sigma_prior+sigma_prior_scaled-sigma_prior_scaled.dot(p.T).dot(inv(p.dot(sigma_prior_scaled).dot(p.T)+omega)).dot(p)
        return (mu_bl,sigma_bl)

    num_assets = len(mu)
    init_guess = num_assets * [1./num_assets,]

    # q is a vector of the view for each stock
    q = 0.1*mu
    # p is an identity matrix with the size of number of assets
    p = np.identity(len(mu))
    mu_bl,sigma_bl=bl(w_prior = init_guess, sigma_prior = Q, p=p, q=q)

    # Optimize weight using mvo with expected returns calculated from black-litterman
    norm_weight, ticker_index = mvo(mu_bl,Q,card)
    return norm_weight, ticker_index
