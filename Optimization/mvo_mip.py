import cvxpy as cp
def mvo_mip (mu, Q, card):
  """
  :param mu: n*1 vector, expected returns of n assets
  :param Q: n*n matrix, covariance matrix of n assets
  :param card: a scalar, cardinality constraint
  :return: norm_weight (the portfolio weight), ticker_index (the indices of selected stock)
  """
  w = cp.Variable(len(mu))
  # z is integer variables for cardinality constraint
  z = cp.Variable(len(mu), integer=True)
  gamma = 0.001
  exp_ret = mu.T * w
  risk = cp.quad_form(w, Q)
  
  # create the objective funtion: Minimize w^T*Q*w - gamma*mu^T*w
  # create the constraints: 1^T*w = 1, 1^T*z = card, L_i*z_i <= x_i <= U_i*z_i where L_i = 0 and U_i = 1, z_i = {0,1}
  prob = cp.Problem(cp.Minimize(risk - gamma * exp_ret),
                    [cp.sum(w) == 1,
                      w >= 0,
                      cp.sum(z) == card,
                     z >= 0,
                     z <= 1])
  prob.solve()
  weight = x.value
  ticker_index = np.argsort(weight)[-card:]
  norm_weight = weight[np.argsort(weight)[-card:]]
  return norm_weight, ticker_index
