import requests as req
from bs4 import BeautifulSoup as beau
import pandas as pd
import csv


# 사이트로부터 리스트 정보 받아오기

url = "https://www.mei-a9.info/cars"
response = req.get(url)

if response.status_code == 200:
    response = req.get(url).text.encode('utf-8')
    response = beau(response, 'html.parser')

    target = response.find('table',{'id':'list', 'class':'table'})
    thead = target.find_all('th')

    theadList = []

    # 사이트 내 th, td 태그 제거 
    theadLen = len(thead)
    for i in range(0, theadLen):
        thead = target.find_all('th')[i].text
        theadList.append(thead)

    tdTags = target.find_all('td')

    rowList=[]
    columnList = []

    tdTagsLen = len(tdTags)
    for i in range(0, tdTagsLen):
        element = str(tdTags[i].text)
        if "  " in element:
            element = element.replace("  ", " ")
            
        columnList.append(element)
        
        if i % 2 ==1:
            rowList.append(columnList)
            columnList=[]
    result = pd.DataFrame(rowList, columns=theadList)
    # 태그 제거 결과 확인
    print(result)

    # csv 파일로 우선 저장 [차량, 클래스] 꼴로 저장됨
    f = open('data/A9 Car List.csv','w',encoding='utf-8',newline='')
    writer = csv.writer(f)
    writer.writerow(theadList)
    writer.writerows(rowList)
    f.close()

else:
    print(f"{url} status : {response.status_code}")