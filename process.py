import requests
import json
import pandas as pd

from parseprocess import _drug_SEInfo_finder


baseURL = 'https://apis.data.go.kr/1471000/MdcinGrnIdntfcInfoService01/getMdcinGrnIdntfcInfoList01?serviceKey=0LDPiRtGED4k%2BHK8n7FPOwhEj4hbxFHCKpdLSWGRKIfFbP7sEC5iITHWOhomPblSk6%2FnQrx2p0HR7lctnOl3iQ%3D%3D'


### 약 성분명을 알 떄 ###

## 입력 데이터 후처리
def process(drugname, userInput):
    inputIndex = ['DRUG_SHAPE', 'COLOR_CLASS1','FORM_CODE_NAME','PRINT_PRONT']
    

    for i in range (4):
        if(userInput[i] == ''):
            inputIndex[i] = '';

    userInput = list(filter(None, userInput))
    inputIndex = list(filter(None, inputIndex))

    print(inputIndex, userInput, len(inputIndex))


    ## api data parsing ##
    url = baseURL + '&item_name=' + drugname +'&type=json'

    response = requests.get(url, verify=False)
    contents = response.text
    jsonData = json.loads(contents)
    jsonData = jsonData['body']['items']

    df=pd.DataFrame(jsonData)

    print(df);

    ## 판다스 부분

    ## result 초기화
    eitem = []
    sideEffect = [[],[]]

    inform = df[['ITEM_SEQ','ITEM_NAME', 'CHART', 'DRUG_SHAPE', 'COLOR_CLASS1']] #정보 불러오기

    if(userInput == []):
        select = inform; #약 특징 입력값이 아무것도 없으면 

    else: #값이 있으면
        for j in range(len(inputIndex)): #인풋 인덱스 크기만큼
            select = inform[inform[inputIndex[j]]==userInput[j]] #긁어온 데이터 값과 같은 것만 골라냄 
        print(select);

    select = select.head(3)

    ditem = select.loc[:,'ITEM_SEQ']
    eitem = ditem.tolist()
    print(eitem)


    for k in range(len(eitem)):
        drugNotice=_drug_SEInfo_finder(eitem[k])
        url = drugNotice[0] 
        drugNotice = drugNotice[1]

        sideEffect[0].append(url)
        sideEffect[1].append(drugNotice)

    return sideEffect


'''
#consol
result = process('이부프로펜',['원형','','','']);
print(result);
#print(_ai_process(result[1]));
'''