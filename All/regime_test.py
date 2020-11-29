class Regime_test (object):
# card = 10
# regime_flag = 0
# regime_flag = 1
# model_flag = 0
# model_flag = 1
# model_flag = 2
# model_flag = 3
# model_flag = 4
# cost_flag = 0
# cost_flag = 1
# date = ['2010-10-15']
# price_table = df
  def cardinality (principal):
    if principal <= 10000:
      card = 5
    elif principal > 10000 and principal <= 100000:
      card = 5
    else: card = 12
    return card
  def choose_model (regime_flag):
    if regime_flag == 0:
      model_flag = 2
      cost_flag = 0
    else:
      model_flag = 1
      cost_flag = 0
    return model_flag, cost_flag
  def get_weight (mu, Q, card, price_table, date, old_weight, old_ticker, model_flag, cost_flag, target_return,lookback,risk_appetite):
    opt_model = [[mvo,mvo_cost],[cvar,cvar_cost],[robust_cvar,robust_cvar_cost],
                [max_sharpe, max_sharpe_cost],[risk_parity, risk_parity_cost]]
    if model_flag == 1 or model_flag == 2:
      if cost_flag == 0:
        weight, ticker_index = opt_model[model_flag][cost_flag](mu,Q,card,price_table,date,target_return,lookback,risk_appetite)
      else:
        weight, ticker_index = opt_model[model_flag][cost_flag](mu,Q, card, price_table, date, old_weight, old_ticker,target_return,lookback,risk_appetite)
    else:
      if cost_flag == 0:
        weight, ticker_index = opt_model[model_flag][cost_flag](mu,Q,card)
      else:
        weight, ticker_index = opt_model[model_flag][cost_flag](mu,Q, card, old_weight, old_ticker)
    return weight, ticker_index

  def multiperiod (factors_return, excess_return, df, lookback, principle,target_return,regimes,risk_appetite,cardinality):
    weight = []
    ticker_index = []
    mu_all = []
    if cardinality == 0:
      card = Regime_test.cardinality(principle)
    else:
      card = cardinality
    
    #model_flag, cost_flag = optimization.choose_model(regime_flag)
    print(len(factors_return),len(excess_return))
    if len(factors_return) % lookback != 0:
      factors_return = factors_return[:-int(len(factors_return) % lookback)]
      excess_return = excess_return[:-int(len(excess_return) % lookback)]
    #print(len(factors_return))
    #print(len(factors_return),len(excess_return))

    for i in range(int(len(factors_return)/lookback)):
      regime_flag = regimes[lookback*(i+1)]
      model_flag, cost_flag = Regime_test.choose_model(regime_flag)
      #print(len(factors_return[i*lookback:(i+1)*lookback]))
      #print(len(excess_return[i*lookback:(i+1)*lookback]))
      # if i <= 3:
      #   mu, Q = factors_fit.generate_factor(factors_return[0:(i+1)*lookback],excess_return[0:(i+1)*lookback])
      # else:
      #   mu, Q = factors_fit.generate_factor(factors_return[(i-3)*lookback:(i+1)*lookback],excess_return[(i-3)*lookback:(i+1)*lookback])
      mu, Q = factors_fit.generate_factor(factors_return[0:(i+1)*lookback],excess_return[0:(i+1)*lookback])
      #print(len(Q))
      if i == 0:
        old_weight = np.zeros(card)
        old_ticker = np.arange(card)
      else:
        old_weight = weight[i-1]
        old_ticker = ticker_index[i-1]
      mu_all.append(mu)
      temp = Regime_test.get_weight(mu,Q,card, df, df.columns.values[(i+1)*lookback], old_weight, old_ticker, model_flag, cost_flag,target_return,lookback,risk_appetite)
      weight.append(temp[0])
      ticker_index.append(temp[1])
    return mu_all, weight, ticker_index
  
  def get_port_info (mu,Q,weight,ticker,date_list):
    #all_weight = []
    #all_ticker = []
    all_exp_return = []
    all_actual_return = []
    all_port_exp_ret = []
    all_port_act_ret = []
    dates = []
    for i in range(len(date_list)-2):
      cur_date = df.columns.values[date_list[i]]
      print(cur_date)
      dates.append(cur_date)
      # exp_return = mu[ticker[i]]
      exp_return = mu[i][ticker[i]]
      if i == 0:
        actual_return = 1
      else:
        actual_return = df.iloc[ticker[i],date_list[i+2]].values/df.iloc[ticker[i],date_list[i+1]].values
      port_exp_return = lookback*sum(weight[i]*exp_return)
      port_actual_return = sum(weight[i]*actual_return)-1
      #all_weight.append(weight[i])
      #all_ticker.append(ticker[i])
      all_exp_return.append(exp_return)
      all_actual_return.append(actual_return)
      all_port_exp_ret.append(port_exp_return)
      all_port_act_ret.append(port_actual_return)
    return dates, all_exp_return, all_actual_return, all_port_exp_ret, all_port_act_ret

  ### Calculate expected and actual cumulative return
  def cum_return (port_ret):
    cal_ret_list = []
    cum_ret_list = []
    cum_ret_list.append(1)
    for i in range(len(port_ret)):
      cal_ret_list.append(port_ret[i]+1)
    ret = 1
    for num in cal_ret_list:
      ret = ret*num
      cum_ret_list.append(ret)
    return cum_ret_list

  # calculate the mean difference between actual and expected return
  def mean_diff (act_ret,exp_ret):
    diff_list = np.asarray(act_ret) - np.asarray(exp_ret)
    return diff_list.mean()

  def sharpe_ratio (act_ret,exp_ret,rf):
    act_std = np.std(act_ret)
    exp_std = np.std(exp_ret)
    act_sr = (np.subtract(act_ret,rf))/act_std
    exp_sr = (np.subtract(exp_ret,rf))/exp_std
    return act_sr, exp_sr

  def get_cum_ret(date_list,lookback,target_return,principle,risk_appetite,card):
    cost_flag = 0
    excess_return, factors_return, regimes, price_table = Regime_test.get_returns(10)
    mu_all, w, t = Regime_test.multiperiod (factors_return[:], excess_return[:], df=price_table, lookback = lookback, principle = principle,target_return = target_return,regimes = regimes,risk_appetite = risk_appetite,cardinality = card)
    #print(mu_all[1][t[1]])
    dates, all_exp_return, all_actual_return, all_port_exp_ret, all_port_act_ret = Regime_test.get_port_info (mu=mu_all,Q=None,weight=w,ticker=t,date_list=date_list)
    # mu_all[0][ticker[1]]
    # print(all_port_act_ret)
    cum_ret_exp = Regime_test.cum_return(all_port_exp_ret)
    cum_ret_act = Regime_test.cum_return(all_port_act_ret)
    all_weight = w
    all_ticker = t
    return dates, all_weight, all_ticker, cum_ret_exp,cum_ret_act
  
  def get_returns(Time_horizon):
    data = factors_fit.read_asset('SP500AdjClose')
    factors = RegimeSwitching.read_factor(start_date = '2005-09-30')
    market_factor = RegimeSwitching.get_marketfactor(factors)
    latent_state = RegimeSwitching.hmm_fit(np.array(market_factor).reshape(-1,1))
    regimes = RegimeSwitching.thresholding_regime(latent_state, 5)
    factors = RegimeSwitching.combine(factors,regimes)
    price_table, return_matrix = factors_fit.asset_return(data)
    [asset_return,factors_return,corresponding_regime] = factors_fit.factors_and_returns(return_matrix,factors)
    excess_return = factors_fit.get_excess_return(asset_return,factors_return)
    return excess_return, factors_return,regimes,price_table
