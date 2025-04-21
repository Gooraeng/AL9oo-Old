# 카헌트 영상 공유
# Last Update : 240130

from discord import app_commands, Interaction, Embed
from discord.ext import commands
from typing import List
from .management.bot_in_channel import check_channel_list, get_no_permission_embed
from .utils import settings
from .utils.embed_log import failed
from .utils.manage_tool import CarhuntRiot as CR
from .utils.not_here import not_here_return_embed


log_channel = int(settings.log_channel)
feedback_log_channel = int(settings.feedback_log_channel)


class CarHunt(commands.Cog):
    def __init__(self, app : commands.Bot) -> None:
        self.app = app
    
    
    @app_commands.command(name='카헌트', description= '카헌트 영상을 보여줍니다!')
    @app_commands.describe(car = '어떤 차량을 고르시나요?')
    @app_commands.rename(car = '차량')
    @app_commands.guild_only()
    async def car_hunt_search(self, interaciton : Interaction, car : str):

        # 로그 채널에 명령어 입력 시 실행을 막는 임베드 출력
        if interaciton.channel.id == log_channel or interaciton.channel.id == feedback_log_channel:
            return await not_here_return_embed(interaction= interaciton)

        if check_channel_list(interaction= interaciton) == False:
            no_permission_embed = get_no_permission_embed()
            return await interaciton.response.send_message(embed= no_permission_embed, ephemeral= True, delete_after= 10)
        
        car = car.upper()
        
        car_data = await CR.CarName_db()
        map_data = await CR.Area_db()
        lap_time_data = await CR.LapTime_db()
        link_data = await CR.Link_db()
    
        
        try:
            # 입력한 차량명과 일치하는 차량의 인덱스 넘버 변수 선언 
            CarName_found = car_data.index(car)
            await interaciton.response.send_message(f'```차량 : {car_data[CarName_found]}\n맵   : {map_data[CarName_found]}\n기록 : {lap_time_data[CarName_found]}```\n{link_data[CarName_found]}')
            
        
        except Exception:
            
            embed1 = Embed(title='❗오류', description=f'< {car} >의 정보가 없습니다. 다시 시도해주세요!', colour= failed)
            embed1.add_field(name='',value='**<경고>** 이 메세지는 20초 뒤에 지워집니다!', inline=False)
            
            await interaciton.response.send_message('', embed= embed1, ephemeral= True, delete_after=20)
            
        
    @car_hunt_search.autocomplete('car')
    async def chs_autocpletion(self,
        interaction : Interaction,
        current : str
    ) -> List[app_commands.Choice[str]]:
        
        car_name = await CR.CarName_db()
        car_name.pop(0)
        
        result = [
            app_commands.Choice(name= choice, value= choice)
            for choice in car_name if current.lower().replace(" ", "") in choice.lower().replace(" ", "")
        ]
        
        if len(result) > 8:
            result = result[:8]
            
        return result



async def setup(app : commands.Bot):
    await app.add_cog(CarHunt(app))
        