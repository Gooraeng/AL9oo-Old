# 후원 링크 전송 명령어
# Last Update : 240130

from discord import app_commands, Interaction
from discord.ext import commands
from .management.bot_in_channel import check_channel_list, get_no_permission_embed
from .utils import settings
from .utils.not_here import not_here_return_embed


log_channel = int(settings.log_channel)
feedback_log_channel = int(settings.feedback_log_channel)
      
class Donation(commands.Cog):
    def __init__(self,app : commands.Bot):
        self.app = app
    
  
    @app_commands.command(name="후원", description="봇 개발자에게 따뜻한 캔 커피 하나 값을 후원해주실 수 있으실까요?")
    async def donate(self, interaction : Interaction):
        
        if interaction.channel.id == log_channel or interaction.channel.id == feedback_log_channel:
            return await not_here_return_embed(interaction= interaction) 
        
        if check_channel_list(interaction= interaction) == False:
            no_permission_embed = get_no_permission_embed()
            return await interaction.response.send_message(embed= no_permission_embed, ephemeral= True, delete_after= 10)      

        await interaction.response.send_message("## 이용해주셔서 매번 감사드립니다!\n\nhttps://twip.kr/gooraeng_", ephemeral= True)   
    

            
    @donate.error
    async def donate_error(self, interaction : Interaction, error : app_commands.AppCommandError):
        ch = self.app.get_channel(log_channel)
        
        if isinstance(error, app_commands.CommandInvokeError):
            pass


              
async def setup(app : commands.Bot):
    await app.add_cog(Donation(app))