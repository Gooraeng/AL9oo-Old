# 클럽 클래시 관련 명령어
# Last Update : 240130

from discord import app_commands, Embed, Interaction, Object
from discord.ext import commands
from typing import List, Optional
from .management.bot_in_channel import check_channel_list, get_no_permission_embed
from .utils import settings
from .utils.embed_log import failed
from .utils.manage_tool import ClubClash as CC
from .utils.not_here import not_here_return_embed
from .utils.paginator import Pagination

import discord
import numpy


log_channel = int(settings.log_channel)
feedback_log_channel = int(settings.feedback_log_channel)    


class Clash(commands.Cog):
    def __init__(self, app : commands.Bot):
        self.app = app

    
    @app_commands.command(name='클크', description='클럽 클래시 지역의 맵의 레퍼런스를 확인할 수 있습니다!')
    @app_commands.describe(area = '찾고자 하는 맵을 찾아보세요!', car_class = '클래스를 선택하세요!', car_name ='차량명 미선택 시 모든 레퍼런스를 보여줍니다')
    @app_commands.rename(area = '맵', car_class = '클래스', car_name = '차량')
    @app_commands.guilds(1151082666670706758, 751643570758484038)
    @app_commands.guild_only()
    async def clashes(self, interaction: Interaction, area : str, car_class : Optional[str] = None, car_name : Optional[str] = None):

        if interaction.channel.id == log_channel or interaction.channel.id == feedback_log_channel:
            return await not_here_return_embed(interaction= interaction)
        
        if check_channel_list(interaction= interaction) == False:
            no_permission_embed = get_no_permission_embed()
            return await interaction.response.send_message(embed= no_permission_embed, ephemeral= True, delete_after= 10)
        
        # ./utils/manage_tool.py 참고
        map_data = await CC.Area_db()
        class_data = await CC.Class_db()
        car_data = await CC.CarName_db()
        link_data = await CC.Link_db()
        lap_time_data = await CC.LapTime_db()
        
        # 임베드 1 선언 (오류)
        embed1 = Embed(title= '어이쿠!', description= f'무언가 잘못되었습니다. 잠시 후에 다시 시도해주세요.',colour= failed)
        embed1.add_field(name='입력 값', value= f'{area} / {car_class} / {car_name}', inline=False)    
        embed1.add_field(name='', value= '**<경고>** 이 메세지는 10초 뒤에 지워집니다!', inline=False)  
          
        
        # veri - asl assistant or asl assistant
        if interaction.channel.id == 1158477800504836147 or interaction.channel.id == 1158749682642714695 or interaction.channel.id == 1168905892469682177 or interaction.channel.id == 1197495060460212224:
            if (area in list(set(map_data))) and (car_class == None) and (car_name == None):
                    
                area_list = list(filter(lambda x: map_data[x] == area, range(len(map_data))))
            
                embeds = []                
                emp_list_1 = [car_data[area_list[x]] for x in range(0, len(area_list))]
                emp_list_2 = [class_data[area_list[x]] for x in range(0, len(area_list))]
                emp_list_3 = [lap_time_data[area_list[x]] for x in range(0, len(area_list))]
                emp_list_4 = [link_data[area_list[x]] for x in range(0, len(area_list))]
                    
                true_class_data = list(set(emp_list_2)); true_class_data.sort()
                
                for j in range(0, len(true_class_data)):
                    embed = Embed(title= f'<:yt:1178651795472527401> {area}', description= f"{true_class_data[j]} 클래스", colour= 0xff0000)
                    num = 1
                    for i in range(0, len(area_list)):
                        if emp_list_2[i] == true_class_data[j]:
                            embed.add_field(name= f"{num}. {emp_list_1[i]}", value= f"[- {emp_list_3[i]}]({emp_list_4[i]})", inline= False)
                            num += 1
                            
                    embeds.append(embed)
                             
                view = Pagination(embeds)
                view._author = interaction.user
                            
                await interaction.response.send_message(embed=view.initial, view= view)


            if car_name == None and (area in list(set(map_data))) and (car_class in list(set(class_data))):
                try:
                    car_class = car_class.upper()
                    
                    car_name_none_embed = Embed(title= "<:yt:1178651795472527401> References (Click car name to watch video)", description= f"1. Area : {area}\n2. Class : {car_class}", colour= 0xFF0000)
                
                    rest_list_1 = list(filter(lambda x: map_data[x] == area, range(len(map_data))))
                
                    emp_list_1 = list()
                
                    for i in range(len(rest_list_1)):
                        emp_list_1.append(class_data[rest_list_1[i]])

                        
                        if class_data[rest_list_1[i]]== car_class:
                            car_name_none_embed.add_field(name= "", value= f"[- `({lap_time_data[rest_list_1[i]]})` {car_data[rest_list_1[i]]}]({link_data[rest_list_1[i]]})\n\n", inline= False)

                    await interaction.response.send_message(embed= car_name_none_embed)
                    
                except:
                            
                    await interaction.response.send_message(embed= car_name_none_embed)
                
                return
            
            
            try:
                
                area_arr = numpy.array(map_data); car_name_arr = numpy.array(car_data)
                area_search = numpy.where(area_arr == area); car_name_search = numpy.where(car_name_arr == car_name)
                same2 = int(numpy.intersect1d(area_search, car_name_search))
                
                car_name = car_name.upper()
                # 정상 실행
                if area == map_data[same2] and car_class == class_data[same2] and car_name == car_data[same2]:
                    return await interaction.response.send_message(f'```차량 : {car_data[same2]}\n맵   : {map_data[same2]}\n기록 : {lap_time_data[same2]}```\n{link_data[same2]}')
                        
                    
                # 임베드 1 출력
                else:
                    return await interaction.response.send_message('', embed= embed1, ephemeral= True, delete_after=10)


            
            # 오류 관리 - 임베드 1 출력 
            except Exception as e:
                return await interaction.response.send_message('', embed= embed1, ephemeral= True, delete_after=10)
                
        
        else:   
            embed2 = Embed(title= '해당 채널에서는 실행하실 수 없습니다.', colour= 0xf51000,
                                    description= 'ASL Assistant 제작자의 승인이 없는 채널은 이용하실 수 없습니다.')
            return await interaction.response.send_message(embed= embed2, ephemeral= True, delete_after= 10)        

    @clashes.error
    async def clashes_error_handling(self, interaction : Interaction, error : app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandInvokeError):
            pass
        elif isinstance(error, discord.HTTPException):
            pass
        elif isinstance(error, discord.NotFound):
            pass
        else : raise error
        
        
    @clashes.autocomplete('area')
    async def area_autocompletion(
        self,
        interaciton : Interaction,
        current : str,
        
    ) -> List[app_commands.Choice[str]]:
        if current == '' :
            return [
                app_commands.Choice(name= 'Search the map regardless of space!', value='Search the map regardless of space!')
            ]
        # 차량 리스트 선언
        map_data = await CC.Area_db()
        
        map_data.pop(0) 
        # 겹치는 차량 리스트가 존재하고, 리스트 검색 시 이를 허용하지 않게 하기 위한
        # set을 이용하여 겹치는 차량이 없는 새 리스트 선언
        filtered = list(set(map_data))

        result1 = [
            app_commands.Choice(name=choice, value=choice)
            for choice in filtered if current.lower().replace(" ", "") in choice.lower().replace(" ", "")
        ]
    
        if len(result1) > 6:
            result1 = result1[:6]
            
        return result1 
        
    
    @clashes.autocomplete('car_class')
    async def class_autocompletion(
        self,
        interaction : Interaction,
        current : str,    
    ) -> List[app_commands.Choice[str]]:
        
        # 리스트 선언
        map_data = await CC.Area_db()
        class_data = await CC.Class_db()
        
        map_data.pop(0) ; class_data.pop(0)
        # area_autocompletion을 통해 찾으려는 맵과 관련된 요소를 불러옴.
        # 여기선 딕셔너리를 이용하여 불러옴 >> dict_values(['Sacred Heart', ''])
        # 리스트로 변환
        aa = list(interaction.namespace.__dict__.values())
        
        # 검색된 맵의 행들을 인덱스로 가지는 리스트를 선언함
        # 이 때, map_data와 aa의 value가 일치하도록 필터링 (aa[0])
        rest_list = list(filter(lambda x: map_data[x] == str(aa[0]), range(len(map_data))))
        
          
        emp_list = list()
        for i in range(len(rest_list)):
            emp_list.append(class_data[rest_list[i]])
        
        # emp_list 내 존재하는 중복 요소 제거
        filetered = list(set(emp_list))
        
        result2 = [
            app_commands.Choice(name= choice,value= choice)
            for choice in filetered if current.lower().replace(" ", "") in choice.lower().replace(" ", "")
        ]
        
        return result2
            
    @clashes.autocomplete(name='car_name')
    async def car_autocompletion(
        self,
        interaction : Interaction,
        current : str, 
    ) -> List[app_commands.Choice[str]]:
        

        # 리스트 선언
        map_data = await CC.Area_db()
        car_data = await CC.CarName_db()
        class_data = await CC.Class_db()
        
        map_data.pop(0); car_data.pop(0); class_data.pop(0)
        # class_autocompletion의 결과와 연동이 어려워 같은 방법 반복
        aa = list(interaction.namespace.__dict__.values())
        rest_list_1 = list(filter(lambda x: map_data[x] == str(aa[0]), range(len(map_data))))
        
        
        emp_list_1 = list(); emp_list_2 = list()
        
        for i in range(len(rest_list_1)):
            emp_list_1.append(class_data[rest_list_1[i]])
            
            if class_data[rest_list_1[i]]== str(aa[1]):
                emp_list_2.append(car_data[rest_list_1[i]])
                
        result3 = [
            app_commands.Choice(name=choice, value=choice)
            for choice in emp_list_2 if current.lower().replace(" ", "") in choice.lower().replace(" ", "")
        ]
        
        if len(result3) > 25:
            result3 = result3[:25]
            
        return result3
    
    
            
async def setup(app: commands.Bot):
    await app.add_cog(Clash(app))
    await app.tree.sync(guild = Object(1151082666670706758))
    await app.tree.sync(guild = Object(751643570758484038))