import requests
from bs4 import BeautifulSoup

itemSeq = '201309204' #품목 코드(코대원)

htmls = requests.get('https://nedrug.mfds.go.kr/pbp/CCBBB01/getItemDetail?itemSeq=' + itemSeq)
bs = BeautifulSoup(htmls.content, 'html.parser')
search_data = bs.find('div', class_='info_box mt30 pt0 notice').get_text(); #사용법 및 주의사항 crawling
print(search_data); 


DrugList = []
url = 'https://terms.naver.com/medicineSearch.naver?mode=exteriorSearch&so=st4.dsc&shape='
htmls = requests.get(url)
bs = BeautifulSoup(htmls.content, 'html.parser')
search_data = bs.find_all('strong', "title") #사용법 및 주의사항 crawDrugListng

for strong in search_data:
    DrugList.append(strong.text) #태그 때고 contect parsing

DrugList = DrugList[5:]
for countI in range(len(DrugList)):
    DrugList[countI] = DrugList[countI].split('\n')[1] #약 이름만 가져오게 sDrugListcing


