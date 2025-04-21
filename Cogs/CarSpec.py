# 차량의 디테일한 성능을 알려주는 명령어
# Last Update : 240130

from discord import app_commands, Embed, File, Interaction
from discord.ext import commands
from typing import List
from .management.bot_in_channel import check_channel_list, get_no_permission_embed
from .utils import manage_tool, settings
from .utils.manage_tool import AboutCar as AC
from .utils.embed_log import succeed, failed, etc
from .utils.not_here import not_here_return_embed

import asyncio


log_channel = int(settings.log_channel)
feedback_log_channel = int(settings.feedback_log_channel)


class CarSpec(commands.Cog):
    def __init__(self, app : commands.Bot):
        self.app = app
    
    
    # 명령어 설명
    @app_commands.command(name= '스펙', description= '차량의 성능을 확인합니다!')
    @app_commands.describe(car= '차량 성능 확인')
    @app_commands.rename(car= '차량')
    @app_commands.guild_only()
    async def car(self, interaction : Interaction, car : str):
        
        if interaction.channel.id == log_channel or interaction.channel.id == feedback_log_channel:
            return await not_here_return_embed(interaction= interaction)

        if check_channel_list(interaction= interaction) == False:
            no_permission_embed = get_no_permission_embed()
            return await interaction.response.send_message(embed= no_permission_embed, ephemeral= True, delete_after= 10)
        
        # 조회 불가능 차량 리트를 불러옴
        car = car.upper()
        get_check_list = await manage_tool.check_update()
        
        
        if get_check_list == None:
            get_check_list_ = '없음'
        
        else:
            get_check_list_ = ('\n* ').join(s for s in get_check_list)
        
        # 정상 실행 임베드 생성
        embed1 = Embed(title='⚠️주의', description=f'정보가 누락되거나 정확하지 않을 수 있습니다. 문제 발견 시 **/feedback**을 통해 신고해주십시오!', colour=0x7fe6e4)
        embed1.add_field(name='',value='스펙시트가 완성되지 않은 차량은 조회하실 수 없습니다!', inline=False)
        embed1.add_field(name='',value='모든 이미지의 출처는 "A9-Database" 디스코드 서버입니다.', inline=False)
        embed1.add_field(name='- 조회 불가능 차량', value= f"* {get_check_list_}", inline= False)
        
       
        # 정상 실행
        try:
            await interaction.response.send_message('', embed=embed1, file=File(f'Car_spec_img/{car}.png'),ephemeral=True)
            
           
        
        # 오류 관리
        except Exception:
                        
            if FileNotFoundError:
                # 리스트 상으로는 존재하나 세부 정보가 없는 차량명 출력
                if car in get_check_list:
                    embed2 = Embed(title= '❗오류', description= f'< {car} >의 정보가 현재 없습니다. 조회 불가능한 차량 리스트를 보고 다시 시도해주세요!', colour= failed)
                    embed2.add_field(name= '- 조회 불가능 차량', value= f"* {get_check_list_}", inline= False)
                    embed2.add_field(name= '', value='**<경고>** 이 메세지는 20초 뒤에 지워집니다!', inline=False)
                    
                    await interaction.response.send_message('', embed= embed2, ephemeral= True, delete_after=20)
                    
  
                # 리스트 상에도 존재하지 않는 차량명 출력
                else:
                    embed3 = Embed(title= '❗오류', description= f'그런 이름의 차량은 없습니다. 다시 시도해주세요!', colour= failed)
                    embed3.add_field(name='', value='**<경고>** 이 메세지는 10초 뒤에 지워집니다!', inline=False)
                    
                    await interaction.response.send_message('', embed= embed3, ephemeral= True, delete_after=10)
                    

            # 기타 오류
            else:
                await interaction.response.defer(ephemeral= True, thinking= True)
                await asyncio.sleep(5)
                
            
                embed4 = Embed(title='❗오류', description=f'지금은 조회할 수 없습니다! 잠시 후에 다시 시도해주세요.',colour= failed)
                await interaction.followup.send(embed= embed4, ephemeral= True)
                

                
                     
    # 리스트 자동 완성 
    @car.autocomplete("car")
    async def car_autocompletion(
        self,
        interaction : Interaction,
        current : str,
    ) -> List[app_commands.Choice[str]]:

        car_list = await AC.utilize_list()
        
        result = [
            app_commands.Choice(name= choice, value= choice)
            for choice in car_list if current.lower().replace(" ", "") in choice.lower().replace(" ", "")
        ]
        
        # Choice 갯수가 10개 초과 시 최대로 보여주는 Choice 수를 10개 까지로 제한
        if len(result) > 8:
            result = result[:8]
                
        return result



async def setup(app : commands.Bot):
    await app.add_cog(CarSpec(app))