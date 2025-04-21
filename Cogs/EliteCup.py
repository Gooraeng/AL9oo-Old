# 엘리트 관련 명령어
# Last Update : 240130

from discord import app_commands, Embed, Interaction
from discord.ext import commands
from typing import Literal, List, Optional
from .management.bot_in_channel import check_channel_list, get_no_permission_embed
from .utils import settings
from .utils.embed_log import failed
from .utils.manage_tool import EliteCup as EC
from .utils.not_here import not_here_return_embed
from .utils.paginator import Pagination

import numpy
import asyncio


log_channel = int(settings.log_channel)
feedback_log_channel = int(settings.feedback_log_channel)

class Elitecup(commands.Cog):
    def __init__(self, app : commands.Bot):
        self.app = app
    
    
    @app_commands.command(name='엘리트', description='엘리트컵 레퍼런스를 알려드립니다!')
    @app_commands.describe(class_type = '어떤 클래스인가요?', car_name ='어떤 차량을 찾아보시겠어요?')
    @app_commands.rename(class_type = '타입', car_name = '차량')
    @app_commands.guild_only()
    async def elite(self, interaction: Interaction, class_type : Literal["S", "A", "B", "C"] = None, car_name : Optional[str] = None):
        if interaction.channel.id == log_channel or interaction.channel.id == feedback_log_channel:
            return await not_here_return_embed(interaction= interaction)
        
        if check_channel_list(interaction= interaction) == False:
            no_permission_embed = get_no_permission_embed()
            return await interaction.response.send_message(embed= no_permission_embed, ephemeral= True, delete_after= 10)
        
        # ./utils/manage_tool.py 참고
        class_data = await EC.Class_db(); class_data.pop(0)
        map_data = await EC.Area_db(); map_data.pop(0)
        car_data = await EC.CarName_db(); car_data.pop(0)
        lap_time_data = await EC.LapTime_db(); lap_time_data.pop(0)
        link_data = await EC.Link_db(); link_data.pop(0)
                
        embed1 = Embed(title='어이쿠!', description=f'무언가 잘못되었습니다. 잠시 후에 다시 시도해주세요.',colour= failed)
        
        
        if (car_name == None) and (class_type == None):
            try:
                class_array = numpy.array(class_data)
                embeds = []                
                true_class_data = list(set(class_data)); true_class_data.sort()
                
                for j in range(0, len(true_class_data)):
                    class_where = numpy.where(class_array == true_class_data[j])
                    class_where = class_where[0].tolist()
                    
                    embed = Embed(title= f"<:yt:1178651795472527401> Elite {true_class_data[j]}", description= f'{map_data[class_where[0]]}',colour= 0xff0000)
                    
                    for i in range(0, len(class_where)):
                        embed.add_field(name= f'{i + 1}. {car_data[class_where[i]]}', value= f'[- {lap_time_data[class_where[i]]}]({link_data[class_where[i]]})', inline= False)

                    
                    embeds.append(embed)
                
                view = Pagination(embeds)
                view._author = interaction.user
                
                await interaction.response.send_message(embed= view.initial, view= view)
            
            except:
                await interaction.response.send_message(embed= embed1, ephemeral= True, delete_after= 10)
                
        embed1.add_field(name= '검색', value= f'{class_type} / {car_name}')                           
        embed1.add_field(name='',value='**<경고>** 이 메세지는 10초 뒤에 지워집니다!', inline=False)  
        
                      
        if class_type is not None and car_name == None:        
            try:
                
                rest_list_1 = list(filter(lambda x: class_data[x] == class_type, range(len(class_data))))
                
                car_name_none_embed = Embed(title= "<:yt:1178651795472527401> References (Click car name to watch video)", description= f"1. Area : {map_data[rest_list_1[0]]}\n2. Class : {class_type}", colour= 0xFF0000)
            
                for i in range(len(rest_list_1)):
                    car_name_none_embed.add_field(name= "", value= f"[- `({lap_time_data[rest_list_1[i]]})` {car_data[rest_list_1[i]]}]({link_data[rest_list_1[i]]})\n\n", inline= False)

                return await interaction.response.send_message(embed= car_name_none_embed)
                
            except:
                        
                await interaction.response.defer(thinking= True)
                await asyncio.sleep(5)
                return await interaction.followup.send(embed= car_name_none_embed)
        
        
        if class_type is not None and car_name is not None:
            try:
                class_arr = numpy.array(class_data)
                car_arr = numpy.array(car_data)
                map_arr_where = numpy.where(class_arr == class_type)
                car_arr_where = numpy.where(car_arr == car_name)
                same_num_list = int(numpy.intersect1d(map_arr_where, car_arr_where))
                car_name = car_name.upper()
                
                # 정상 실행
                if class_type == class_data[same_num_list]:
                    if car_name == car_data[same_num_list]:
                        await interaction.response.send_message(f'```차량 : {car_data[same_num_list]}\n맵   : {map_data[same_num_list]}\n기록 : {lap_time_data[same_num_list]}```\n{link_data[same_num_list]}')
                    
                        
                    else:
                        await interaction.response.send_message('', embed= embed1, ephemeral= True, delete_after=10)

                # 오류(알맞지 않은 입력) - 임베드 1 출력
                else:
                    await interaction.response.send_message('', embed= embed1, ephemeral= True, delete_after=10)

            
            # 오류(알맞지 않은 입력) - 임베드 1 출력 
            except Exception:
                await interaction.response.send_message('', embed= embed1, ephemeral= True, delete_after=10)
    

                    
    @elite.autocomplete(name= 'car_name')
    async def area_autocompletion(
        self,
        interaction : Interaction,
        current : str,    
    ) -> List[app_commands.Choice[str]]:
        
        # 리스트 선언
        class_type_data = await EC.Class_db()
        car_data = await EC.CarName_db()
        
        class_type_data.pop(0); car_data.pop(0)
        # class_type_autocompletion을 통해 찾으려는 맵과 관련된 요소를 불러옴.
        # 여기선 딕셔너리를 이용하여 불러옴 >> dict_values(['Weekly Competition', ''])
        # 리스트로 변환
        aa = list(interaction.namespace.__dict__.values())
        
        # 검색된 맵의 행들을 인덱스로 가지는 리스트를 선언함
        # 이 때, map_data와 aa의 value가 일치하도록 필터링 (aa[0])
        rest_list = list(filter(lambda x: class_type_data[x] == str(aa[0]), range(len(class_type_data))))
           
        emp_list = list()
        for i in range(len(rest_list)):
            emp_list.append(car_data[rest_list[i]])
        
        # emp_list 내 존재하는 중복 요소 제거
        filetered = list(set(emp_list))
        
        result2 = [
            app_commands.Choice(name=choice,value=choice)
            for choice in filetered if current.lower().replace(" ", "") in choice.lower().replace(" ", "")
        ]
        
        if len(result2) > 25:
            result2 = result2[:25]
            
        return result2

        

    
async def setup(app : commands.Bot):
    await app.add_cog(Elitecup(app))