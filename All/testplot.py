import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
class testplot(object):  
  ### Plot weight distribution as pie chart
  #matplotlib inline
  def plot_pie(weight, ticker,df):
    labels = df.index.values[ticker]
    sizes = weight
    # Creating plot 
    # fig, (ax1, ax2) = plt.subplots(1, 2)
    # fig.suptitle('portfolio weight')
    # ax1.pie(sizes_mvo, labels = labels_mvo) 
    # ax2.pie(sizes_cvar, labels = labels_cvar)
    # ax1.title.set_text('MVO')
    # ax2.title.set_text('CVaR')
    #explode = (0, 0.1, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,0)  # only "explode" the 2nd slice (i.e. 'Hogs')

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.show()

  ### Plot acutal and expected return
  #matplotlib inline

  def backtest_plot (date_list, all_port_act_ret, all_port_exp_ret):
    fig, ax = plt.subplots()
    loc = plticker.MultipleLocator(base=90) # this locator puts ticks at regular intervals
    ax.xaxis.set_major_locator(loc)
    ax.plot(date_list[:-3],all_port_act_ret[:-1],date_list[:-3],all_port_exp_ret[:-1],'b')
    # ax.set_xticklabels(['2010','2010','2012','2014','2016','2018','2020'])
    ax.set_xlabel('Date')
    ax.set_ylabel('Return(%)')
    ax.set_title('Backtesting of Portfolio Return')
    ax.legend(['Actual Return','Expected Return'])

  ### Plot cumulative portfolio return
  #matplotlib inline
  def cum_plot (date_list, cum_ret_exp, cum_ret_act):
    fig, ax = plt.subplots()
    loc = plticker.MultipleLocator(base=90) # this locator puts ticks at regular intervals
    ax.xaxis.set_major_locator(loc)
    # y = np.sin(x)
    ax.plot(date_list[:-2],np.asarray(cum_ret_exp)*100-100,date_list[:-2],np.asarray(cum_ret_act)*100-100)
    ax.set_xlabel('Date')
    ax.set_ylabel('Return (%)')
    ax.set_title('Cumulative Portfolio Return')
    ax.legend(['Cumulated Expected Return','Cumulated Actual Return'])
    ax.set_xticklabels(['2010','2010','2012','2014', '2016','2018','2020'])
