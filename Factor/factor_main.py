
import json 
import csv 
import numpy as np
import requests
import csv
import json
import pandas as pd
import datetime as dt
import sys
import os
import pymongo
import argparse
import dns

from Database.database_main import Database
factors = Database.read_data('factors')

print(factors)
newfactor = factors[factors["date"] >= '2005-09-30']
newfactor = newfactor.sort_values(by=['date'])
factors_return = newfactor.values.tolist()
print(factors_return[:5])

market_factor = []
for cols in factors_return:
  market_factor.append(cols[1])
lookback = 5
regimes = [0] * len(market_factor)
for i in range(len(regimes)):
  if i>=lookback:   #say lookback = 5
    temp = market_factor[i-lookback:i]
    #print(temp)
    if all(elem >= -10 for elem in temp):   #Pass bull market condition
      regimes[i] = 1 #Switch to Bull Market
    
    
      
import numpy as np
from itertools import accumulate
class RegimeSwitching(object):
  class HMM:
      def __init__(self, n_state, n_obs, S=None, A=None, B=None):
          self.n_state = n_state  # number of state
          self.n_obs = n_obs  # number of observation
          self.S = S  # 1*n, the initial distribution
          self.A = A  # n*n, the transition matrix
          self.B = B  # n*m, Emission matrix


  def _alpha(hmm, obs, t):
      # calculate alpha at time t
      b = hmm.B[:, obs[0]]
      alpha = np.array([hmm.S * b])  # n*1
      for i in range(1, t + 1):
          alpha = (alpha @ hmm.A ) * np.array([hmm.B[:, obs[i]]])
      return alpha[0]


  def fancyGamma(hmm, obs, t):
      # calculate alpha at time t
      b = hmm.B[:, obs[0]]
      fancyGamma = np.array([hmm.S * b])  # n*1
      for i in range(1, t + 1):
          fancyGamma = (fancyGamma @ hmm.A) * np.array([hmm.B[:, obs[i]]])
      return fancyGamma[0]

  def forward_prob1(hmm, obs):
      # sum of all the states
      alpha = _alpha(hmm, obs, len(obs) - 1)
      return np.sum(alpha,axis = 1)

  def forward_prob(hmm, obs):
      # sum of all the states
      alpha = _alpha(hmm, obs, len(obs) - 1)
      return np.sum(alpha)


  def _beta(hmm, obs, t):
      # calculate beta at time t
      beta = np.ones(hmm.n_state)
      for i in reversed(range(t + 1, len(obs))):
          beta = np.sum(hmm.A * hmm.B[:, obs[i]] * beta, axis=1)
      return beta


  def backward_prob(hmm, obs):
      # sum up
      beta = _beta(hmm, obs, 0)
      return np.sum(hmm.S * hmm.B[:, obs[0]] * beta)


  def fb_prob(hmm, obs, t=None):
      # put together forward and backwards
      if t is None:
          t = 0
      res = _alpha(hmm, obs, t) * _beta(hmm, obs, t)
      return res.sum()


  def _gamma(hmm, obs, t):
      # calculate the probability of each state at time t
      alpha = _alpha(hmm, obs, t)
      beta = _beta(hmm, obs, t)
      prob = alpha * beta
      return prob / prob.sum()


  def point_prob(hmm, obs, t, i):
      # calculate the probability at state i, at time t. 
      prob = _gamma(hmm, obs, t)
      return prob[i]


  def _xi(hmm, obs, t):
      alpha = np.mat(_alpha(hmm, obs, t))
      beta_p = _beta(hmm, obs, t + 1)
      obs_prob = hmm.B[:, obs[t + 1]]
      obs_beta = np.mat(obs_prob * beta_p)
      alpha_obs_beta = np.asarray(alpha.T * obs_beta)
      xi = alpha_obs_beta * hmm.A
      return xi / xi.sum()


  def fit(hmm, obs_data, maxstep=500):
      # Baum-Welch
      hmm.A = np.ones((hmm.n_state, hmm.n_state)) / hmm.n_state
      hmm.B = np.ones((hmm.n_state, hmm.n_obs)) / hmm.n_obs
      hmm.S = np.random.sample(hmm.n_state)  #Random initialization
      hmm.S = hmm.S / hmm.S.sum()
      step = 0
      while step < maxstep:
          xi = np.zeros_like(hmm.A)
          gamma = np.zeros_like(hmm.S)
          B = np.zeros_like(hmm.B)
          S = _gamma(hmm, obs_data, 0)
          for t in range(len(obs_data) - 1):
              tmp_gamma = _gamma(hmm, obs_data, t)
              gamma += tmp_gamma
              xi += _xi(hmm, obs_data, t)
              B[:, obs_data[t]] += tmp_gamma

          # update A
          for i in range(hmm.n_state):
              hmm.A[i] = xi[i] / gamma[i]
          # update B
          tmp_gamma_end = _gamma(hmm, obs_data, len(obs_data) - 1)
          gamma += tmp_gamma_end
          B[:, obs_data[-1]] += tmp_gamma_end
          for i in range(hmm.n_state):
              hmm.B[i] = B[i] / gamma[i]
          # update S
          hmm.S = S
          step += 1
      return hmm


  def predict(hmm, obs):
      # Viterbi
      N = len(obs)
      nodes_graph = np.zeros((hmm.n_state, N), dtype=int)  
      delta = hmm.S * hmm.B[:, obs[0]]  
      nodes_graph[:, 0] = range(hmm.n_state)

      for t in range(1, N):
          new_delta = []
          for i in range(hmm.n_state):
              temp = [hmm.A[j, i] * d for j, d in enumerate(delta)]  # Current state = i, and go back one state
              max_d = max(temp) #Find optimal last step's emission
              new_delta.append(max_d * hmm.B[i, obs[t]]) #Emit at that last time
              nodes_graph[i, t] = temp.index(max_d) #Take the argmax. 
          delta = new_delta

      current_state = np.argmax(nodes_graph[:, -1])
      path = []
      t = N
      while t > 0:
          path.append(current_state)
          current_state = nodes_graph[current_state, t - 1]
          t -= 1
      return list(reversed(path))
  def read_factor():
    factors = Database.read_data('factors')
    return factors
  
  def filter_factor(factors):
    newfactor = factors[factors["date"] >= '2005-09-30']
    newfactor = newfactor.sort_values(by=['date'])
    return newfactor
  
  def get_marketfactor(newfactor):
    factors_return = newfactor.values.tolist()
    print(factors_return[:5])

    market_factor = []
    for cols in factors_return:
      market_factor.append(cols[1])
    return market_factor
  def thresholding_regime(market_factor, lookback):
    regimes = [0] * len(market_factor)
    for i in range(len(regimes)):
      if i>=lookback:   #say lookback = 5
        temp = market_factor[i-lookback:i]
        if all(elem >= -0.2 for elem in temp):   #Pass bull market condition
          regimes[i] = 1 #Switch to Bull Market
    return regimes

  def combine(newfactor,regimes):
    newfactor['Regime'] = regimes
    return newfactor

    
    
          
factors = RegimeSwitching.read_factor()
newfactor = RegimeSwitching.filter_factor(factors)
market_factor = RegimeSwitching.get_marketfactor(newfactor)
regimes = RegimeSwitching.thresholding_regime(market_factor, 5)
result = RegimeSwitching.combine(newfactor,regimes)

zer = 0
one = 0
for num in regimes:
  if num == 0:
    zer += 1
  else:
    one += 1
print(zer)
print(one)

import numpy as np 
from numpy.linalg import inv
from numpy import matmul
import cvxopt
import numpy
from cvxopt import matrix
from copy import deepcopy
class matrix_helper(object):

  def add_to_each_row(matrix, index, to_add):
    '''
      For each row of matrix, add to_add to the position of index and shift the rest.
      Example:
        add_to_each_row([[1,2],[3,4]], 1, 5) returns [[1,5,2],[3,5,4]]
    '''
    for i in range(len(matrix)):
      if index >= len(matrix[0]) or index < 0:
        return
      matrix[i] = matrix[i][:index] + [to_add] + matrix[i][index:]


  def add_to_each_ele(matrix, to_add):
    '''
      Add to_add to each element of the matrix
    '''
    for i in range(len(matrix)):
      for j in range(len(matrix[i])):
        matrix[i][j] += to_add

  def remove_negative(matrix):
    '''
      Add to_add to each element of the matrix
    '''
    for i in range(len(matrix)):
      for j in range(len(matrix[i])):
        if matrix[i][j] <= 0:
          matrix[i][j] = 0.000000001
    return matrix


  def cvxopt_solve_qp(P, q, G=None, h=None, A=None, b=None):
      P = .5 * (P + P.T)  # make sure P is symmetric
      args = [matrix(P), matrix(q)]
      if G is not None:
          args.extend([matrix(G), matrix(h)])
          if A is not None:
              args.extend([matrix(A), matrix(b)])
      sol = cvxopt.solvers.qp(*args)
      if 'optimal' not in sol['status']:
          return None
      return numpy.array(sol['x']).reshape((P.shape[1],))


  def get_correlation_from_covariance_matrix(Q):
    '''
      Given covariance matrix Q, return the correlation matrix rho.
    '''
    rho = deepcopy(Q)
    for i in range(len(rho)):
      for j in range(len(rho[0])):
        rho[i][j] = Q[i][j] / ((Q[i][i] * Q[j][j]) ** 0.5)
    return rho


  def transpose(matrix):
    if len(matrix) == 0:
      return []
    trans = []
    for i in range(len(matrix[0])):
      trans.append([0] * len(matrix))
    for i in range(len(matrix)):
      for j2 in range(len(matrix[0])):
        try:
          trans[j2][i] = matrix[i][j2]
        except:
          import pdb; pdb.set_trace()
    return trans


import copy
from scipy.stats.mstats import gmean
import numpy as np
from numpy import matmul
from numpy.linalg import inv
class factors_fit(object):
  
    def read_asset(universe):
      return Database.read_data(universe)
  
    def asset_return(price):
      price = price.dropna()
      price.set_index(keys=['Symbol'], drop=False,inplace=True)
  
      cols = []
      for col in price.columns: 
          if col != 'Symbol' and col != '_id':
            cols.append(col)
      #print(cols)
  
      missing = pd.concat([price[c] == 0 for c in cols], axis=1).any(axis=1)
  
      df_with_missing = price[missing]
      #print(df_with_missing.shape)  #Remove the first 10
      df_not_missing = price[~missing]
      #print(df_not_missing.shape) 
      df = df_not_missing[cols]
      #print(df)
      import numpy as np
      datanp = df.values.astype(np.float32)
      ret = df.pct_change(axis = 1)
      ret = ret.drop(['2005-09-30'],axis =1)  #Change if date change
      return ret.values.tolist()
  
    def factors_and_returns(asset_return,factors_return):
      factors_return = factors_return[0:len(factors_return):5]       #can change if factors match exactly
      factors_return = factors_return.drop(columns = ['date'])
      factors_return = factors_return.values.tolist()
      for i in range(len(asset_return)):
        if len(asset_return[i]) > len(factors_return):
          asset_return[i] = asset_return[i][:len(factors_return)]
        else:
          factors_return = factors_return[:len(asset_return[i])]
      for row in factors_return:
        del row[6]
        #del row[5]
      return asset_return,factors_return
  
    def get_excess_return(asset_return_matrix,factor_returns):
      for i in range(len(asset_return_matrix)):
        to_minus = factor_returns[i][5]  #Rf in factor return
        for j in range(len(asset_return_matrix[i])):
          asset_return_matrix[i][j] -= to_minus
      return matrix_helper.transpose(asset_return_matrix)
  
  
  
    def generate_factor(factor_returns, asset_returns):
      '''
        Input:
          factor_returns: a matrix of factor returns in the specified period, without the first column being 1.
                  For example, a two day three-factor factor returns is 
                  [[0.1, 0.2, 0.5],
                  [-0.2, 0.3, -0.02]]
                  Note that the date is not present, the first element is just day 1. 
                  The caller of the function is responsible for matching the date between the asset return
                  and the factor return.
          
          asset_returns: 	This is asset's excess return with respect to risk-free rate. Each column is the asset's
                  excess return for example, a universe with three stocks and two days may look like
                  [[0.05,0.02,-0.08],
                  [0.1, -0.2, 0.25]]
                  each column is a stock's excess return in these two days, again, day is relative and is 
                  caller's reponsibility.
        Output:
          expected_return: n x 1 vector standing for asset expected returns, n being the number of assets
          covariance_matrix: n x n matrix representing the covariance matrix for n assets.
      '''
      factor_returns_w_1 = copy.deepcopy(factor_returns)
      matrix_helper.add_to_each_row(factor_returns_w_1, 0, 1)
      factor_returns_w_1 = np.array(factor_returns_w_1)
      factor_returns_w_1_T = factor_returns_w_1.transpose()
      try:
        reg_res = matmul(matmul(inv(matmul(factor_returns_w_1_T, factor_returns_w_1)), factor_returns_w_1_T), asset_returns)
      except:
        import pdb; pdb.set_trace()
      alphas = reg_res[0]
      betas = reg_res[1:]
      expected_factor_return = factors_fit.get_expected_factor_return(factor_returns)
      factor_returns_T = np.array(factor_returns).transpose()
      factor_covariance = np.cov(factor_returns_T)
      epsilon = np.subtract(asset_returns, matmul(factor_returns_w_1, reg_res))
      epsilon = epsilon.transpose()
      residual_var_matrix = np.diag(np.diag(np.cov(epsilon)))
      expected_return = np.add(alphas, matmul(betas.transpose(), expected_factor_return))
      covariance_matrix = np.add(matmul(matmul(betas.transpose(), factor_covariance), betas), residual_var_matrix)
      return expected_return, covariance_matrix
      
  
    def get_expected_factor_return(factor_returns):
      factor_returns_added_1 = copy.deepcopy(factor_returns)
      matrix_helper.add_to_each_ele(factor_returns_added_1, 1)
      factor_returns_added_1 = matrix_helper.remove_negative(factor_returns_added_1)
      #print(factor_returns_added_1)
      expected_factor_return = []
      factor_returns_added_1 = np.array(factor_returns_added_1).transpose()
      for i in range(len(factor_returns_added_1)):
        expected_factor_return.append(gmean(factor_returns_added_1[i]) - 1)
      return expected_factor_return

data = factors_fit.read_asset('SP500Price')
factors = RegimeSwitching.read_factor()
newfactor = RegimeSwitching.filter_factor(factors)
market_factor = RegimeSwitching.get_marketfactor(newfactor)
regimes = RegimeSwitching.thresholding_regime(market_factor, 5)
factors = RegimeSwitching.combine(newfactor,regimes)
return_matrix = factors_fit.asset_return(data)
asset_return,factors_return = factors_fit.factors_and_returns(return_matrix,factors)
excess_return = factors_fit.get_excess_return(asset_return,factors_return)

mu, Q = factors_fit.generate_factor(factors_return,excess_return)

print(np.shape(Q))
print(np.shape(mu))
