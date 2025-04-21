# 차량 및 크럽 클래시
# Last Update : 240130

import csv
import os, sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


# 차량 정보 함수
class AboutCar:        
    async def utilize_list():
        data = list()
        f = open('data/A9 Car List.csv', "r",encoding='utf-8',newline='')
        reader = csv.reader(f)
        for row in reader:
            data.append(row[0])
        data.pop(0)
        f.close()
        return data

    async def make_car_img_list():
        car_img_list  = list()
        for filename in os.listdir('Car_spec_img'):
            if filename.endswith(".png") or filename.endswith(".jpg"):
                car_img_list.append(filename[:-4])
            elif filename.endswith(".jpeg"):
                car_img_list.append(filename[:-5])
        return car_img_list

# 클럽 클래시 유틸 함수
class ClubClash:                
    async def Area_db():
        data  = list()
        f = open('data/Club Clash Database.csv', "r",encoding='utf-8',newline='')
        reader = csv.reader(f)
        for row in reader:
            data.append(row[0])
        f.close()
        return data

    async def CarName_db():
        data = list()
        f = open('data/Club Clash Database.csv', "r",encoding='utf-8',newline='')
        reader = csv.reader(f)
        for row in reader:
            data.append(row[1])
        f.close()
        return data

    async def Class_db():
        data = list()
        f = open('data/Club Clash Database.csv', "r",encoding='utf-8',newline='')
        reader = csv.reader(f)
        for row in reader:
            data.append(row[2])
        f.close()
        return data
        
    async def LapTime_db():
        data = list()
        f = open('data/Club Clash Database.csv', "r",encoding='utf-8',newline='')
        reader = csv.reader(f)
        for row in reader:
            data.append(row[3])
        f.close()
        return data
        
    async def Link_db():
        data = list()
        f = open('data/Club Clash Database.csv', "r",encoding='utf-8',newline='')
        reader = csv.reader(f)
        for row in reader:
            data.append(row[4])
        f.close()
        return data



# WeeklyCompetition 관리 함수
class WeeklyCompetition:
    async def Area_db():
        data  = list()
        f = open('data/WeeklyCompetition DB.csv', "r" ,encoding= 'utf-8',newline= '')
        reader = csv.reader(f)
        for row in reader:
            data.append(row[0])
        f.close()
        return data
 
    
    async def CarName_db():
        data  = list()
        f = open('data/WeeklyCompetition DB.csv', "r" ,encoding= 'utf-8',newline= '')
        reader = csv.reader(f)
        for row in reader:
            data.append(row[1])
        f.close()
        return data

    
    async def LapTime_db():
        data  = list()
        f = open('data/WeeklyCompetition DB.csv', "r" ,encoding= 'utf-8',newline= '')
        reader = csv.reader(f)
        for row in reader:
            data.append(row[3])
        f.close()
        return data
 
    
    async def Link_db():
        data  = list()
        f = open('data/WeeklyCompetition DB.csv', "r" ,encoding= 'utf-8',newline= '')
        reader = csv.reader(f)
        for row in reader:
            data.append(row[4])
        f.close()
        return data



# EliteCup 관리 함수
class EliteCup:
    async def Class_db():
        data  = list()
        f = open('data/EliteCup DB.csv', "r" ,encoding= 'utf-8',newline= '')
        reader = csv.reader(f)
        for row in reader:
            data.append(row[0])
        f.close()
        return data
    
    
    async def Area_db():
        data  = list()
        f = open('data/EliteCup DB.csv', "r" ,encoding= 'utf-8',newline= '')
        reader = csv.reader(f)
        for row in reader:
            data.append(row[1])
        f.close()
        return data
    
    
    async def CarName_db():
        data  = list()
        f = open('data/EliteCup DB.csv', "r" ,encoding= 'utf-8',newline= '')
        reader = csv.reader(f)
        for row in reader:
            data.append(row[2])
        f.close()
        return data
    
    
    async def LapTime_db():
        data  = list()
        f = open('data/EliteCup DB.csv', "r" ,encoding= 'utf-8',newline= '')
        reader = csv.reader(f)
        for row in reader:
            data.append(row[3])
        f.close()
        return data
    
    
    async def Link_db():
        data  = list()
        f = open('data/EliteCup DB.csv', "r" ,encoding= 'utf-8',newline= '')
        reader = csv.reader(f)
        for row in reader:
            data.append(row[4])
        f.close()
        return data
    
    
        
# TLE 관리 함수
class TimeLimitedEventData:
    
    # EN 
    async def type_of_tle():
        data  = list()
        f = open('data/TLE DB.csv', "r",encoding='utf-8',newline='')
        reader = csv.reader(f)
        for row in reader:
            data.append(row[0])
        f.close()
        return data


    async def Area_db():
        data = list()
        f = open('data/TLE DB.csv', "r",encoding='utf-8',newline='')
        reader = csv.reader(f)
        for row in reader:
            data.append(row[1])
        f.close()
        return data


    async def CarName_db():
        data = list()
        f = open('data/TLE DB.csv', "r",encoding='utf-8',newline='')
        reader = csv.reader(f)
        for row in reader:
            data.append(row[2])
        f.close()
        return data

        
    async def LapTime_db():
        data = list()
        f = open('data/TLE DB.csv', "r",encoding='utf-8',newline='')
        reader = csv.reader(f)
        for row in reader:
            data.append(row[4])
        f.close()
        return data

        
    async def Link_db():
        data = list()
        f = open('data/TLE DB.csv', "r",encoding='utf-8',newline='')
        reader = csv.reader(f)
        for row in reader:
            data.append(row[5])
        f.close()
        return data



# carhunt 관리 함수
class CarhuntRiot:                
    async def CarName_db():
        data = list()
        f = open('data/Car hunt DB.csv', "r",encoding='utf-8',newline='')
        reader = csv.reader(f)
        for row in reader:
            data.append(row[0])
        f.close()
        return data
 
    
    async def Area_db():
        data = list()
        f = open('data/Car hunt DB.csv', "r",encoding='utf-8',newline='')
        reader = csv.reader(f)
        for row in reader:
            data.append(row[1])
        f.close()
        return data

        
    async def LapTime_db():
        data = list()
        f = open('data/Car hunt DB.csv', "r",encoding='utf-8',newline='')
        reader = csv.reader(f)
        for row in reader:
            data.append(row[3])
        f.close()
        return data

        
    async def Link_db():
        data = list()
        f = open('data/Car hunt DB.csv', "r",encoding='utf-8',newline='')
        reader = csv.reader(f)
        for row in reader:
            data.append(row[4])
        f.close()
        return data



class Specialevent:
    async def CarName_db():
        data = list()
        f = open('data/SpecialEvent DB.csv', "r",encoding='utf-8',newline='')
        reader = csv.reader(f)
        for row in reader:
            data.append(row[0])
        f.close()
        return data
 
    
    async def Area_db():
        data = list()
        f = open('data/SpecialEvent DB.csv', "r",encoding='utf-8',newline='')
        reader = csv.reader(f)
        for row in reader:
            data.append(row[1])
        f.close()
        return data

        
    async def LapTime_db():
        data = list()
        f = open('data/SpecialEvent DB.csv', "r",encoding='utf-8',newline='')
        reader = csv.reader(f)
        for row in reader:
            data.append(row[3])
        f.close()
        return data

        
    async def Link_db():
        data = list()
        f = open('data/SpecialEvent DB.csv', "r",encoding='utf-8',newline='')
        reader = csv.reader(f)
        for row in reader:
            data.append(row[4])
        f.close()
        return data



# 업데이트 확인 > car_spec에 활용
async def check_update():
    data_csv = await AboutCar.utilize_list() 
    data_img = await AboutCar.make_car_img_list()
    
    # 업데이트 된 차량(들)의 리스트 선언 
    check_new = list(set(data_csv)- set(data_img))
    if len(list(data_csv))-len(list(data_img))==0:
        return check_new == None
    else:
        return check_new



# 업데이트 확인 > 최초 실행 시 콘솔에 출력
async def print_CP():
    
    data_csv = await AboutCar.utilize_list() 
    data_img = await AboutCar.make_car_img_list()

    # 업데이트 된 차량(들)의 리스트 선언 
    check_new = list(set(data_csv)- set(data_img))
    
    # 리스트 대조 후 일치 시
    # KTM X-BOW GTX는 이미 존재하는 차량인데 data 리스트에서는 띄어쓰기가 두 번 적용된 것이 확인되어 억지로 맞게 만듬
    if len(list(data_csv))-len(list(data_img))==0:
        return print('추가된 차량이 없습니다!')

    # 리스트 대조 후 불일치 시
    # 89번 줄과 같은 사유
    else:
        return print('차량 업데이트 발견: '+ str(check_new))
