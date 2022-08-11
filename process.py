import pandas as pd

import matplotlib
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def _pandas_processing(excelData):
    ### pandas Part ###

    #data input
    excel_url = './static/excel/' + excelData;
    DF = pd.read_excel(excel_url);
    
    #data process
    DF.index = DF.index + 1; #1부터 시작하게....
    x = DF['x']
    y = DF['y']
    z = DF['z']
    velocity = DF['속력']

    first = DF.loc[:, ['x','y','z']].head(1)
    first = first.values[0];
    last = DF.loc[:, ['x','y','z']].tail(1)
    last = last.values[0];

    ### graph ###
    #처음과 끝에 빨간 점 찍어 이동 방향 indicate

    ## Common: 폰트 설정 
    fm.get_fontconfig_fonts()
    font_location = './static/fonts/NanumGothicBold.ttf' # For Windows
    font_name = fm.FontProperties(fname=font_location).get_name()
    matplotlib.rc('font', family=font_name)

    plt.switch_backend('agg') # backend switch

    ## velocity
    plt.plot(velocity.index, velocity, label = '속도')

    #design
    plt.legend()
    plt.xlabel('시간')
    plt.ylabel('속력')

    #save
    plt.savefig('./static/img/result/velocity.png')

    ## MOVE
    fig = plt.figure(figsize=(9, 6))
    ax = fig.add_subplot(111, projection='3d')

    #start-end indicate ball
    ax.scatter(first[0], first[1], first[2], color='red')
    ax.scatter(last[0], last[1], last[2], color='red')

    ax.plot(x, y, z, label='move')
    #design
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.legend()

    ##save
    plt.savefig('./static/img/result/move.png');

""" 
#console
dataname = 'move.xlsx'
_pandas_processing(dataname);
plt.show();
 """