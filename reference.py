import imp
import pandas as pd
import numpy as np

import matplotlib
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

import FinanceDataReader as fdr

### pandas Part ###




    ### graph Part ###

        plt.switch_backend('agg') # backend switch

        ## Common: 폰트 설정 
        fm.get_fontconfig_fonts()
        font_location = './static/fonts/NanumGothicBold.ttf' # For Windows
        font_name = fm.FontProperties(fname=font_location).get_name()
        matplotlib.rc('font', family=font_name)


        ## P/F Graph
        plt.figure(1)

        #graph making
        barWidth = 0.25;
        PF_x = np.array(list(range(0, sheetSize)), dtype=float);

        passBar = plt.bar(PF_x, waferResult[:, 0], color='blue', width=barWidth, label='Pass'); # passchip graph
        failBar = plt.bar(PF_x+barWidth, waferResult[:, 1], color='red',width=barWidth, label = 'Fail'); # failchip graph
        plt.xticks(PF_x+(barWidth/2), testCount);

        #design
        plt.xlabel('테스트 횟수');
        plt.ylabel('개수');
        plt.title('P/F Result');
        plt.legend(); #범례

        #number labeling
        for countI in passBar:
            height = countI.get_height()
            plt.text(countI.get_x() + countI.get_width()/2.0, height, '%d' % height, ha='center', va='bottom', size = 9)

        for countJ in failBar:
            height = countJ.get_height()
            plt.text(countJ.get_x() + countJ.get_width()/2.0, height, '%d' % height, ha='center', va='bottom', size = 9)

        ##save
        plt.savefig('./static/img/result/PF.png');


        ## Yield Graph -> require AI process
        plt.figure(2);

        #graph making
        plt.plot(testCount, waferYield, color='blue',linestyle='--',marker='o')

        #design
        plt.xlabel('테스트 횟수') #x 라벨
        plt.ylabel('Yield(단위: %)') #y 라벨
        plt.title("WaferYield") #그래프 이름
        plt.ylim(1,100)

        #number labeling
        for countK in range(sheetSize):
            height = waferYield[countK]
            plt.text(testCount[countK], height + 3, '%.2f' %height, ha='center', va='bottom', size = 9)

        ##save
        plt.savefig('./static/img/result/Yield.png');

        #Yield 1st indicate part
        #Yield가 설정 입력 미만이면 ai 판단결과와 상관 없이 양산 불가 판정
        failWafer = 0;

        for countI in range(sheetSize):
            if(waferYield[countI] < yieldLimit):
                failWafer += 1;
        

        if(failWafer > (sheetSize/2)): #수율이 너무 낮은 wafer가 과반수 이상일 때
            failWafer = -1; #-1 : 양산 실패로 check

        return failWafer