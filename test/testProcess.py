import pandas as pd

import matplotlib
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

dataname = 'move.xlsx'

### pandas Part ###
def _pandas_exchange_processing(excelData):
    #data input
    excel_url = './static/excel/' + excelData;
    DF = pd.read_excel(excel_url);
    #data process
    x = DF['x']
    y = DF['y']
    z = DF['z']

    fig = plt.figure(figsize=(9, 6))
    ax = fig.add_subplot(111, projection='3d')

    ## graph
    #plt.switch_backend('agg') # backend switch

    ## Common: 폰트 설정 
    fm.get_fontconfig_fonts()
    font_location = './static/fonts/NanumGothicBold.ttf' # For Windows
    font_name = fm.FontProperties(fname=font_location).get_name()
    matplotlib.rc('font', family=font_name)

    ax = fig.add_subplot(111, projection='3d')
    
    ax.plot(x, y, z, label='move')

    #design
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.legend()

    ##save
    plt.savefig('./static/img/result/move.png');


#console
_pandas_exchange_processing(dataname);
