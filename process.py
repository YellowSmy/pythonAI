import matplotlib
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt


def _pandas_processing(input):
    ### graph ###

    right = input.count(-1);
    left = input.count(1);
    data = [left, right];
    ## Common: 폰트 설정 
    fm.get_fontconfig_fonts()
    font_location = './static/fonts/NanumGothicBold.ttf' # For Windows
    font_name = fm.FontProperties(fname=font_location).get_name()
    matplotlib.rc('font', family=font_name)

    #plt.switch_backend('agg') # backend switch

    ## L/R graph
    plt.figure(1);
    plt.bar([0,1], data, color=['r', 'b'], width=0.5);
    plt.xticks([0,1], ['Left', 'Right'])

    #design
    plt.legend()
    plt.xlabel('Left/Right')
    plt.ylabel('Count')

    #save
    plt.savefig('./static/img/result/LRresult.png')


    ##indicate Graph
    plt.figure(2);
    plt.plot([1,2,3,4,5], input, color='green');
    
    #save
    plt.savefig('./static/img/result/LRIndi.jpg');
    

"""
#console
_pandas_processing([1,1,-1,1,-1]);
plt.show();
"""