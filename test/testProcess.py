import requests
import json
import pandas as pd

import matplotlib
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

from parseprocess import _drug_SEInfo_finder

drugName = '몬테루카스트나트륨'
shape = '원형'
color = '주황'
front = ''
back = ''
drugForm = ''

drugList = ['카소딜정', '알피나정', '바스로틴정']

baseURL = 'https://apis.data.go.kr/1471000/MdcinGrnIdntfcInfoService01/getMdcinGrnIdntfcInfoList01?serviceKey=0LDPiRtGED4k%2BHK8n7FPOwhEj4hbxFHCKpdLSWGRKIfFbP7sEC5iITHWOhomPblSk6%2FnQrx2p0HR7lctnOl3iQ%3D%3D'

## result 
refineDF = pd.DataFrame()
item_seq = []
sideEffect = []
#성분명을 모를 때
if(drugList[0] == 'drugFinder'):
    for countI in range(len(drugList)-1):
        
        ## api data parsing ##
        url = baseURL + '&item_name=' + drugList[countI+1] +'&type=json'

        response = requests.get(url, verify=False)
        contents = response.text
        jsonData = json.loads(contents)
        jsonData = jsonData['body']['items']

        ## pandas part ##
        df = pd.DataFrame(jsonData) #JSON to DF
        mediInfoDF = df.loc[:, ['ITEM_NAME','ITEM_SEQ','ITEM_IMAGE', 'ENTP_NAME', 'CHART', 'ETC_OTC_NAME']] #약 사용 정보
        refineDF = refineDF.append(mediInfoDF) 
           
    item_seq = refineDF.loc[:, 'ITEM_SEQ'].values #품목기준번호 for 사이드 이펙트

#약 성분명을 알 떄
else: 
    #입력값 후처리
    InputDrugInfo = {'index' : ['PRINT_FRONT','PRINT_BACK','COLOR_CLASS1','COLOR_CLASS2','DRUG_SHAPE', 'FORM_CODE_NAME'],'value' : [front, back, color, color, shape, drugForm]}
    InputDrugInfo = pd.DataFrame(InputDrugInfo)
    InputDrugInfo = InputDrugInfo.drop(InputDrugInfo[InputDrugInfo['value'] == ''].index) #value가 공백이면 날리기(검색용 인덱스 both)

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
    sideEffect.append(drugNotice)

#console
print(refineDF, item_seq)

# 약 글자 -> 앞뒷면 구분 X sol 필요 -> OR문으로 여러개 나누기(노가다)
#함수 2개로 처리? -> upload 창도 2개로 분리, 더깔끔!
