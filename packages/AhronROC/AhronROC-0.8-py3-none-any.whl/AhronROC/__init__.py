def AhronROC(filename,Sec,k):
    import pandas as pd
    import matplotlib as plt
    import datetime

#data visualization package
    from matplotlib.pyplot import subplots
#date formatter
    from matplotlib.dates import DateFormatter
#tick label formatter
    import matplotlib.ticker as mticker
    Sec_L = ['VXO Index','VXN Index','SPX Index', 'CCMP Index', 'RTY Index', 'MID Index', 'SML Index', 'NYA Index', 'INDU Index', 'VIX Index']
    m=str(k)+'-Day ROC'
    Chart_Title_B = ['1-Day ROC', '2-Day ROC', '3-Day ROC', '5-Day ROC', '10-Day ROC', '20-Day ROC', '30-Day ROC', '50-Day ROC']
    df_main = pd.read_excel(filename)
    df_main.drop(df_main.index[0:3],axis=0,inplace=True)
    df_main['NumofDays'] = range(len(df_main))
   
    for i in Sec_L:
        for j, k in zip(Chart_Title_B, [1, 2, 3, 5, 10, 20, 30, 50]):
            df_main[(i, '{}'.format(j))] = df_main[(i)].pct_change(k)
    df_main.rename(columns = {'Unnamed: 0':'Date'}, inplace = True)
    # print(df_main.columns)
    df_P = df_main[['Date',Sec, 'NumofDays']].dropna()
    df_P['Consecutive'] = df_P['NumofDays'].diff().values

    if df_P['Consecutive'].max() > 20:
        df_P = df_P[df_P.index > df_P[df_P['Consecutive']>20].dropna().index[0]]

    # print(df_main['NYA Index'])
    last_x = df_P[(Sec)].iloc[-30:].max()
    signal_dates = df_P[df_P[(Sec)] >= last_x]
    signal_dates['Consecutive'] = signal_dates['NumofDays'].diff().values

    # filter out signals that occured within 30 days of each other
    signal_dates = signal_dates[(signal_dates.Consecutive>=30)|(signal_dates.Consecutive.isna()==True)]

    # create positive and negative arrays
    df_P['Positive'] = df_main[(Sec,m)].apply(lambda x: 0 if x > 0 else x)
    df_P['Negative'] = df_main[(Sec,m)].apply(lambda x: 0 if x < 0 else x)  
    Chart_Title_T = 'S&P 500 Index'

    fig, (ax1,ax2) = subplots(2, 1, figsize=(20,8.5))

    # closing prices in top chart
    ax1.plot(df_P['Date'],
         df_P[(Sec)], 
         linewidth=2,
         color=[165/255,165/255,165/255],
         label='{} {} {:.2%}'.format(m, '>', last_x))
    ax1.set_title('{}'.format(Chart_Title_T), loc='left', fontweight='bold', fontsize=11)
    ax1.set_yscale('log')
    ax1.tick_params(axis='y', right=True, which='minor', labelright=True, labelsize=9)

    if (df_P.iloc[0]['Date']) < pd.to_datetime('1/1/1990'):
         ax1.yaxis.set_major_formatter(mticker.ScalarFormatter())
         ax1.minorticks_off()
    else:
         ax1.yaxis.set_major_formatter(mticker.NullFormatter())
         ax1.yaxis.set_minor_formatter(mticker.ScalarFormatter())
         
    ax1.grid(visible=True, which='both', linestyle='--')

    plt.text(0.75, 0.89, 'Daily Data: ({} - {})'.format(df_P.iloc[0]['Date'].strftime("%m/%d/%Y"), 
                                                 df_P.iloc[-1]['Date'].strftime("%m/%d/%Y")),
         fontsize=8,  transform=plt.gcf().transFigure)

    if len(signal_dates) < 30:
    #signal name legend
         legend1 = ax1.legend(loc='upper left',handlelength=0, handletextpad=0)
         ax1.legend(['# of Instances: {}\n{dates_or_num}'.format(len(signal_dates),
                    dates_or_num = signal_dates['Date'].apply(lambda x: datetime.datetime.strftime(x, '%m/%d/%Y')).to_string(index=False))],
                loc='upper right',
                handlelength=0,
                handletextpad=0,
                bbox_to_anchor=(1.13, 1.1),
                prop={'size': 10})
         ax1.add_artist(legend1)
         for j in range(len(signal_dates)):
                arrow_date = signal_dates.index[j]
                arrow_price = df_P[(Sec)][df_P.index==arrow_date].iloc[0]
                ax1.annotate("",
                 xy=(arrow_date,
                 arrow_price * 0.99),
                 xytext=(arrow_date,
                    arrow_price * 0.98),
                 horizontalalignment='center',
                 verticalalignment='bottom',
                 fontweight='bold',
                 arrowprops=dict(arrowstyle='->, head_width=.3, head_length=.3',
                            color=[68/255,84/255,106/255],
                            lw=3,))

    ax2.plot(df_P['Date'],
            df_P['Positive'],
            linewidth = 4,
            color =[68/255,84/255,106/255],
            zorder = 0)

    #negative bars             
    ax2.plot(df_P['Date'],
            df_P['Negative'],
            linewidth = 4,
            color =[188/255,108/255,37/255],
            zorder = 0)

    #bottom chart title
    ax2.set_title('{}, {}: {:.2%}'.format(m,
                    df_P.iloc[-1]['Date'].strftime("%m/%d/%Y"),
                    df_P['Positive'].iloc[-1]),
                loc='left',
                fontweight='bold',
                fontsize = 11,
                y=-0.10)

    #y-axis tick labels
    ax2.tick_params(axis = 'y',
                right=True, 
                labelright=True, 
                labelsize=9)
    ax2.yaxis.set_major_formatter(mticker.PercentFormatter(1))

    #grid
    ax2.grid(True, 
            linestyle='--',
            zorder = 0)

    #line from latest reading
    plt.annotate("",
            xy=(df_P.index[-1],
                signal_dates[(Sec)].iloc[-1]),
            xytext=(df_P.index[1],
                    signal_dates[(Sec)].iloc[-1]),
            arrowprops=dict(arrowstyle='-',
                            color=[40/255,54/255,24/255],
                            lw=2,))

    #hide x-axis lables
    ax2.set_xticklabels([])



