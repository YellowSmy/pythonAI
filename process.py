import requests
import json
import pandas as pd

import matplotlib
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

from parseprocess import _drug_SEInfo_finder, _drug_finder

baseURL = 'https://apis.data.go.kr/1471000/MdcinGrnIdntfcInfoService01/getMdcinGrnIdntfcInfoList01?serviceKey=0LDPiRtGED4k%2BHK8n7FPOwhEj4hbxFHCKpdLSWGRKIfFbP7sEC5iITHWOhomPblSk6%2FnQrx2p0HR7lctnOl3iQ%3D%3D'

### 약 성분명을 알 떄 ###
def _pandas_processI(drugName, input):
    ## result 초기화
    refineDF = pd.DataFrame()
    item_seq = []
    sideEffect = [[],[]]

    #입력값 후처리
    InputDrugInfo = {'index' : ['PRINT_FRONT','PRINT_BACK','COLOR_CLASS1','COLOR_CLASS2','DRUG_SHAPE', 'FORM_CODE_NAME'],'value' : input}
    InputDrugInfo = pd.DataFrame(InputDrugInfo)
    InputDrugInfo = InputDrugInfo.drop(InputDrugInfo[(InputDrugInfo['value'] == '') | (InputDrugInfo['value'] == 'none')].index) #value가 공백이면 날리기(검색용 인덱스 both)

    ## api data parsing ##
    url = baseURL + '&item_name=' + drugName +'&type=json'

    response = requests.get(url, verify=False)
    contents = response.text
    jsonData = json.loads(contents)
    jsonData = jsonData['body']['items']

    ## pandas part ##
    df = pd.DataFrame(jsonData) #JSON to DF 
    drugDF = df.loc[:, ['PRINT_FRONT','PRINT_BACK','COLOR_CLASS1','COLOR_CLASS2','DRUG_SHAPE', 'FORM_CODE_NAME']] # 약 모양 정보
    #글자(앞면, 뒷면), 색상(앞면, 뒷면), 약 모양, 제형

    mediInfoDF = df.loc[:, ['ITEM_NAME','ITEM_SEQ','ITEM_IMAGE', 'ENTP_NAME', 'CHART', 'ETC_OTC_NAME']] #약 사용 정보 
    #약 이름, 품목기준번호, 이미지, 회사명, 성상(약 모양), 전문/일반 구분

    if(InputDrugInfo.empty == True): #성분명 외 다른 조건이 없을 경우
        refineDF = mediInfoDF
    
    else: #성분명외 다른 조건이 있을 경우
        for countI in range(len(InputDrugInfo.index)):
            index = InputDrugInfo.iloc[countI]['index']
            value = InputDrugInfo.iloc[countI]['value']
            refineDF = refineDF.append(mediInfoDF[drugDF[index] == value]) #약 모양 정보 DB량 비교, 약 사용 정보 불러오기

    
    if(len(refineDF.index) > 3): #refineDF 검색결과가 3개 이상이면 최상위 3개만 보여주기
        refineDF = refineDF.head(3);

    item_seq = refineDF.loc[:, 'ITEM_SEQ'].values #품목기준번호 for 사이드 이펙트
    
    ## S/E part ##
    for countJ in range(len(item_seq)): 
        drugNotice = _drug_SEInfo_finder(item_seq[countJ])
        url = drugNotice[0] #부작용 출력 위한 주소
        drugNotice = drugNotice[1] #부작용 text
        
        sideEffect[0].append(url)
        sideEffect[1].append(drugNotice)

    return sideEffect

### 성분명을 모를 때 ###
def _pandas_processII(input):
    ## result 초기화
    refineDF = pd.DataFrame()
    item_seq = []
    sideEffect = [[],[]]    

    #약 정보 가져오기
    drugList = _drug_finder(input);

    for countI in range(len(drugList)):
        
        ## api data parsing ##
        url = baseURL + '&item_name=' + drugList[countI] +'&type=json'
        response = requests.get(url, verify=False)
        contents = response.text
        jsonData = json.loads(contents)
        jsonData = jsonData['body']['items'] #정보 없으면 넘어오지 않음 -> try -except 구문 쓸것...

        ## pandas part ##
        df = pd.DataFrame(jsonData) #JSON to DF
        mediInfoDF = df.loc[:, ['ITEM_NAME','ITEM_SEQ','ITEM_IMAGE', 'ENTP_NAME', 'CHART', 'ETC_OTC_NAME']] #약 사용 정보
        refineDF = refineDF.append(mediInfoDF) 


    if(len(refineDF.index) > 3): #refineDF 검색결과가 3개 이상이면 최상위 3개만 보여주기
        refineDF = refineDF.head(3);
         
    item_seq = refineDF.loc[:, 'ITEM_SEQ'].values #품목기준번호 for 사이드 이펙트

    ## S/E part ##
    for countJ in range(len(item_seq)): 
        drugNotice = _drug_SEInfo_finder(item_seq[countJ])
        url = drugNotice[0] #부작용 출력 위한 주소
        drugNotice = drugNotice[1] #부작용 text
        
        sideEffect[0].append(url)
        sideEffect[1].append(drugNotice)

    return sideEffect


#console
""" drugName = '몬테루카스트나트륨'
input = ['','','','','',''] #input 순서: 글자(앞면, 뒷면), 색상(앞면, 뒷면), 약 모양, 제형(생략O)
#r= print(_pandas_processII(['1',' ','1',' ',' ']))
r=_pandas_processI(drugName, input)
print(len(r[1][1]))
 """

