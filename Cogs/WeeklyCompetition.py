# 주간 경쟁 관련 명령어
# Last Update : 240130

from discord import app_commands, Embed, Interaction
from discord.ext import commands
from typing import Optional, List
from .management.bot_in_channel import check_channel_list, get_no_permission_embed
from .utils import settings
from .utils.embed_log import failed
from .utils.manage_tool import WeeklyCompetition as WC
from .utils.not_here import not_here_return_embed

import asyncio
import numpy


log_channel = int(settings.log_channel)
feedback_log_channel = int(settings.feedback_log_channel)


class Weeklycompetion(commands.Cog):
    def __init__(self, app : commands.Bot):
        self.app = app
    
    @app_commands.command(name= '주경', description= '주간 경쟁 레퍼런스를 보여드립니다!')
    @app_commands.describe(area= '맵을 고르세요!', car_name= '어떤 차량을 찾아보시겠어요?')
    @app_commands.rename(area= '맵', car_name= '차량')
    @app_commands.guild_only()
    async def weeklycompete(self, interaction: Interaction, area : str, car_name : Optional[str] = None):
        if interaction.channel.id == log_channel or interaction.channel.id == feedback_log_channel:
            return await not_here_return_embed(interaction= interaction)
        
        # ./utils/manage_tool.py 참고
        
        if check_channel_list(interaction= interaction) == False:
            no_permission_embed = get_no_permission_embed()
            return await interaction.response.send_message(embed= no_permission_embed, ephemeral= True, delete_after= 10)
        
        
        map_data = await WC.Area_db(); map_data.pop(0)
        car_data = await WC.CarName_db(); car_data.pop(0)
        lap_time_data = await WC.LapTime_db(); lap_time_data.pop(0)
        link_data = await WC.Link_db(); link_data.pop(0)
        
        map_arr = numpy.array(map_data); car_arr = numpy.array(car_data)
            
        embed1 = Embed(title='어이쿠!', description=f'무언가 잘못되었습니다. 잠시 후에 다시 시도해주세요.',colour= failed)             
        embed1.add_field(name= '검색', value= f'{area} / {car_name}')
        embed1.add_field(name='',value='**<경고>** 이 메세지는 10초 뒤에 지워집니다!', inline=False)  
        
        
        if car_name == None and (area in list(set(map_data))):
            try:
                car_name_none_embed = Embed(title= "<:yt:1178651795472527401> References (Click car name to watch video)", description= f"1. Area : {area}", colour= 0xFF0000)
            
                rest_list_1 = list(filter(lambda x: map_data[x] == area, range(len(map_data))))

                for i in range(len(rest_list_1)):
                    car_name_none_embed.add_field(name= "", value= f"[- `({lap_time_data[rest_list_1[i]]})` {car_data[rest_list_1[i]]}]({link_data[rest_list_1[i]]})\n\n", inline= False)

                await interaction.response.send_message(embed= car_name_none_embed)
                
            except:
                await interaction.response.defer()
                asyncio.sleep(5)
                await interaction.followup.send(embed= car_name_none_embed)
            
            return
        
        # 임베드 1 선언 (오류)
           

        # 정상 실행
        try:
            car_name = car_name.upper()
            
            map_arr_where = numpy.where(map_arr == area)
            car_arr_where = numpy.where(car_arr == car_name)
            same_num_list = int(numpy.intersect1d(map_arr_where, car_arr_where))
            
            if area == map_data[same_num_list] and car_name == car_data[same_num_list]:
                return await interaction.response.send_message(f'```차량 : {car_data[same_num_list]}\n맵   : {map_data[same_num_list]}\n기록 : {lap_time_data[same_num_list]}```\n{link_data[same_num_list]}')
                    
           
                
            return

        # 오류(알맞지 않은 입력) - 임베드 1 출력
        except:  
            return await interaction.response.send_message('', embed= embed1, ephemeral= True, delete_after=10)

            
    @weeklycompete.autocomplete(name= 'area')
    async def area_autocompletion(
        self,
        interaction : Interaction,
        current : str,    
    ) -> List[app_commands.Choice[str]]:
        
        # 리스트 선언
        map_data = await WC.Area_db()
        
        map_data.pop(0)
        
        # emp_list 내 존재하는 중복 요소 제거
        filetered = list(set(map_data))
        
        result1 = [
            app_commands.Choice(name=choice,value=choice)
            for choice in filetered if current.lower().replace(" ", "") in choice.lower().replace(" ", "")
        ]
        
        if len(result1) > 8:
            result1 = result1[:8]
            
        return result1

            
    @weeklycompete.autocomplete(name='car_name')
    async def car_autocompletion(
        self,
        interaction : Interaction,
        current : str, 
    ) -> List[app_commands.Choice[str]]:
        
        # 리스트 선언
        map_data = await WC.Area_db()
        car_data = await WC.CarName_db()
        
        map_data.pop(0); car_data.pop(0)

        aa = list(interaction.namespace.__dict__.values())
        
        rest_list = list(filter(lambda x: map_data[x] == str(aa[0]), range(len(map_data))))
         
        emp_list = list()
        for i in range(len(rest_list)):
            emp_list.append(car_data[rest_list[i]])

                
        result2 = [
            app_commands.Choice(name=choice,value=choice)
            for choice in emp_list if current.lower().replace(" ", "") in choice.lower().replace(" ", "")
        ]
        
        if len(result2) > 10:
            result2 = result2[:10]
            
        return result2
        

    
async def setup(app : commands.Bot):
    await app.add_cog(Weeklycompetion(app))