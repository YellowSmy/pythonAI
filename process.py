from matplotlib import dates
import yfinance as yf
import pandas as pd

import matplotlib 
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
from matplotlib import dates


#2003-12-01 -> 최대 정보
#달러 기준 환율을 원 기준 변환하기
#달러/원 데이터 받아서 나누기...

#USD + 통화 -> 1달러 기준 통화 가치
#통화/KRW -> 통화 기준 KRW 가치 but 연산은 KRW 나누기 통화!
def _pandas_exchange_processing(selectRate, start_date, end_date, selectTime):
    data = yf.download(['USD' + selectRate + '=X'], start=start_date, end=end_date)  #USD/통화 가치 정보 
    KRWData = yf.download(['USDKRW=X'], start=start_date, end=end_date) #USD/KRW 가치 정보

    #달러/원은 특수 경우! -> 바로 출력
    if selectRate == 'USD':
        refineData = pd.Series(KRWData[selectTime])
    else:
        data = pd.Series(data[selectTime]); KRWData = pd.Series(KRWData[selectTime])
        refineData = KRWData / data #통화/KRW 정보 얻기
    refineData.name = selectRate + '/KRW'

    #특잇값 제거(값 튀는거 평균값 대체) IQR process
    q1 = refineData.quantile(0.25)
    q3 = refineData.quantile(0.75)
    iqr = q3-q1

    condition = refineData > q3 + (1.5 * iqr)
    sigma = refineData[condition].index
    refineData.drop(sigma, inplace=True)

    #excel 저장 불필요시 삭제할 것!
    #refineData.to_excel('./static/csv/exchange.xlsx');

    ## graph
    plt.switch_backend('agg') # backend switch

    ## Common: 폰트 설정 
    fm.get_fontconfig_fonts()
    font_location = './static/fonts/NanumGothicBold.ttf' # For Windows
    font_name = fm.FontProperties(fname=font_location).get_name()
    matplotlib.rc('font', family=font_name)


    plt.plot(refineData, color='red', label=refineData.name) 

    #design
    plt.xlabel('연도') #x 라벨
    plt.ylabel('환율') #y 라벨
    plt.title("Exchange Rate") #그래프 이름
    plt.legend();

    #x축 design
    startDay = pd.to_datetime(start_date)
    endDay = pd.to_datetime(end_date)
    period = endDay - startDay
    
    if(period.days > 31): #한달 넘게 조회 시 연도 표시, 달별 sub 눈금
        xData = dates.YearLocator()
        xFormat = dates.DateFormatter('%Y')
        xSub = dates.MonthLocator()
        plt.xticks(rotation=45)

    else: #한달 조회 시 달별 눈금, 일변 sub 눈금
        xData = dates.MonthLocator()
        xFormat = dates.DateFormatter('%Y/%m')
        xSub = dates.DayLocator()

    ax = plt.gca()
    ax.xaxis.set_major_locator(xData)
    ax.xaxis.set_major_formatter(xFormat)
    ax.xaxis.set_minor_locator(xSub);

    ax.set_xlim(left=startDay,right=endDay) # 조회 일자에 맞는 xlimit 설정

    ##save
    plt.savefig('./static/img/result/exchange.png');

""" 
#console
f=_pandas_exchange_processing('RUB', '2003-12-01', '2022-07-30', 'Close');
plt.show();
print(f)   """