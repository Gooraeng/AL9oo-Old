# 최신 패치노트 출력하는 명령어
# Last Update : 240130

from discord import Interaction, app_commands, Embed, Interaction, ui
from discord.ext import commands
from .management.bot_in_channel import check_channel_list, get_no_permission_embed
from .utils import settings
from .utils.embed_log import failed, etc
from .utils.not_here import not_here_return_embed
from .utils.print_time import get_UTC
from .utils.renew_patchnote import get_patchnote_embed

import asyncio


log_channel = int(settings.log_channel)
feedback_log_channel = int(settings.feedback_log_channel)


class buttonfuc(ui.View):
    def __init__(self):
        super().__init__(timeout= None)
        self.add_item(ui.Button(label= '패치노트 보기!', url= 'https://asphaltlegends.com/news'))
    
    
class GetPatchNote(commands.Cog):
    def __init__(self, app : commands.Bot) -> None:
        self.app = app
        
    
    @app_commands.command(name= '최신패치노트', description= '가장 최신의 패치 노트를 알려줍니다')
    @app_commands.checks.cooldown(1, 600, key= lambda i :(i.guild_id, i.user.id))
    @app_commands.guild_only()
    async def send_patchnote(self, interaction : Interaction):
        
        if interaction.channel.id == log_channel or interaction.channel.id == feedback_log_channel:
            return await not_here_return_embed(interaction= interaction) 
        
        if check_channel_list(interaction= interaction) == False:
            no_permission_embed = get_no_permission_embed()
            return await interaction.response.send_message(embed= no_permission_embed, ephemeral= True, delete_after= 10)
        
        title = await get_patchnote_embed()
        time = await get_UTC()
        
        if title == None:
            error_embed = Embed(title= '오류', description= '조회할 수 없습니다. 다시 시도해주세요!', colour= failed)
            await interaction.response.send_message(embed= error_embed, ephemeral= True, delete_after= 10)
     
            
        
        else:
            try:
                await interaction.response.send_message(embed= title, view= buttonfuc())
            
            except Exception:
                await interaction.response.defer(thinking= True)
                await asyncio.sleep(5)
                await interaction.followup.send(embed= title, view= buttonfuc())
            
    
    @send_patchnote.error
    async def srl_error(self, interaction : Interaction, error : app_commands.AppCommandError):
        title = await get_patchnote_embed()
        
        if isinstance(error, app_commands.CommandInvokeError):
            if title == None:
                pass
            
            else:
                pass
        
        if isinstance(error, app_commands.CommandOnCooldown):
            embed_cd_error = Embed(title= '어이쿠! 아직 이용하실 수 없습니다!',
                                           description= f'{int(error.retry_after // 60)}분 {int(error.retry_after % 60)}초 후에 다시 시도해주세요!',
                                           colour= failed)
            await interaction.response.send_message(embed= embed_cd_error, delete_after=5, ephemeral= True)
            
            
    


async def setup(app : commands.Bot):
    await app.add_cog(GetPatchNote(app))