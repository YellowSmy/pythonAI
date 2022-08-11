import requests
from bs4 import BeautifulSoup

"""
    약 code 기준
    선택X(전체) - 공백
    shape(약 모양): 1-10(원형, 타원, 반원, 삼각형, 사각, 마름모, 장방, 오각, 육각, 팔각), 99(기타), 전체- 선택 X
    color: 코드가 길다.. 시키자
    dosageForm(제형): 1-3 (정제류, 경질캡슐, 연질캡슐)
    divisionLine(분할선): 없음(8), -형(2), +형(1), 기타(4) 
"""

#NAVER 의약품 정보로 약 모양으로 약 찾기
def _drug_finder(shape, color, dosageForm, divisionDrugListne, print):
    drugList = [] 
    url = 'https://terms.naver.com/medicineSearch.naver?mode=exteriorSearch&so=st4.dsc' #관련도 순 정렬 주소 
    url = url + '&shape='+shape+'&color='+color+'&dosageForm='+dosageForm+'&divisionDrugListne='+divisionDrugListne+'&identifier='+print
    htmls = requests.get(url)
    bs = BeautifulSoup(htmls.content, 'html.parser')
    search_data = bs.find_all('strong', "title") #사용법 및 주의사항 crawDrugListng

    for strong in search_data:
        drugList.append(strong.text) #태그 때고 contect parsing

    drugList = drugList[5:]
    for countI in range(len(drugList)):
        drugList[countI] = drugList[countI].split('\n')[1] #약 이름만 가져오게 sDrugListcing
        drugList[countI] = drugList[countI].split('mg')[0] #mg 단위 자르기 -> api는 한글..

    drugList.insert(0, 'drugFinder') # drugFinder를 사용했음을 알림
    return drugList;



#품목기준번호로 약품 부작용정보 찾기 for ai process
def _drug_SEInfo_finder(itemSeq):
    htmls = requests.get('https://nedrug.mfds.go.kr/pbp/CCBBB01/getItemDetail?itemSeq=' + itemSeq)
    bs = BeautifulSoup(htmls.content, 'html.parser')
    sideEffect = bs.find('div', class_='info_box mt30 pt0 notice').get_text(); #사용법 및 주의사항 crawling    
    return sideEffect


""" #console
result = _drug_finder('1',' ','1',' ',' ')
print(result) """