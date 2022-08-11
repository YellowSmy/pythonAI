import FinanceDataReader as fdr
import pandas as pd

import matplotlib
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

### pandas Part ###

def _pandas_exchange_processing(selectRate, period, selectTime):
    #exchange
    #data process
    exchangeDF = fdr.DataReader(selectRate, period);
    print(exchangeDF)    

    exchangeDF.to_csv('./static/csv/exchange.csv', mode='w');

    ## graph
    plt.switch_backend('agg') # backend switch

    ## Common: 폰트 설정 
    fm.get_fontconfig_fonts()
    font_location = './static/fonts/NanumGothicBold.ttf' # For Windows
    font_name = fm.FontProperties(fname=font_location).get_name()
    matplotlib.rc('font', family=font_name)


    plt.plot(exchangeDF[selectTime], color='red', label=selectRate) 

    #design
    plt.xlabel('연도') #x 라벨
    plt.ylabel('환율') #y 라벨
    plt.title("Exchange Rate") #그래프 이름
    plt.legend();

    ##save
    plt.savefig('./static/img/result/exchange.png');

""" 
def _pandas_stock_processing():
    #stock 
    stockDF = fdr.StockListing('KOSPI');
    print(stockDF.loc[:, ['Symbol', 'Market', 'Name']]) #html 출력 
"""



#console
_pandas_exchange_processing('USD/KRW', '1981-07', 'Close');
plt.show();
