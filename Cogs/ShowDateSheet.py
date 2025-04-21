# 향후 일정 사진을 출력하는 명령어
# Last Update : 240130

from discord import app_commands, Embed, File, Interaction
from discord.ext import commands
from .management.bot_in_channel import check_channel_list, get_no_permission_embed
from .utils import settings
from .utils.embed_log import succeed
from .utils.not_here import not_here_return_embed


log_channel = int(settings.log_channel)
feedback_log_channel = int(settings.feedback_log_channel)


class ShowDateSheet(commands.Cog):
    def __init__(self, app : commands.Bot):
        self.app = app
    
    
    @app_commands.command(name= '일정', description= '향후 일정을 확인하실 수 있습니다!')
    @app_commands.guild_only()
    async def show_date(self, interaction : Interaction):
        
        if interaction.channel.id == log_channel or interaction.channel.id == feedback_log_channel:
            return await not_here_return_embed(interaction= interaction)
        
        if check_channel_list(interaction= interaction) == False:
            no_permission_embed = get_no_permission_embed()
            return await interaction.response.send_message(embed= no_permission_embed, ephemeral= True, delete_after= 10)
        
        
        embed = Embed(title='**<주의>**', description='* 일정이 정확하지 않을 수 있으니, 그저 참고만 해주세요!',colour= succeed)
        embed.add_field(name= '- 기간', value= '* 231213 ~ 240220', inline= False)
        
        await interaction.response.send_message('', embed = embed, ephemeral = True, file = File('./images/datesheet.png'))


async def setup(app : commands.Bot):
    await app.add_cog(ShowDateSheet(app))