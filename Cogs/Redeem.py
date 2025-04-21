# 리딤 링크를 출력하는 명령어
# Last Update : 240130

from discord import Interaction, app_commands
from discord.ext import commands
from .management.bot_in_channel import check_channel_list, get_no_permission_embed
from .utils import settings
from .utils.not_here import not_here_return_embed


log_channel = int(settings.log_channel)
feedback_log_channel = int(settings.feedback_log_channel)

redeem_link = 'https://www.gameloft.com/redeem/asphalt-9-redeem'


class Redeem(commands.Cog):
    def __init__(self, app : commands.Bot) -> None:
        self.app = app
        
    
    @app_commands.command(name= '리딤', description= '리딤 링크를 알려줍니다')
    async def send_redeem_link(self, interaction : Interaction):
        
        if interaction.channel.id == log_channel or interaction.channel.id == feedback_log_channel:
            return await not_here_return_embed(interaction= interaction) 
        
        if check_channel_list(interaction= interaction) == False:
            no_permission_embed = get_no_permission_embed()
            return await interaction.response.send_message(embed= no_permission_embed, ephemeral= True, delete_after= 10)
        
        await interaction.response.send_message(content= redeem_link, ephemeral= True)
    
    @send_redeem_link.error
    async def srl_error(self, interaction : Interaction, error : app_commands.AppCommandError):
        
        if isinstance(error, app_commands.CommandInvokeError):
            pass
    


async def setup(app : commands.Bot):
    await app.add_cog(Redeem(app))