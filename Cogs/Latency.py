# 봇의 레이턴시 및 메세지 전송 간 딜레이 확인
# Last Update : 240130

from discord import Interaction, app_commands, Embed
from discord.ext import commands
from .management.bot_in_channel import check_channel_list, get_no_permission_embed
from .utils import settings
from .utils.embed_log import failed
from .utils.not_here import not_here_return_embed
from .utils.print_time import get_datetime


log_channel = int(settings.log_channel)
feedback_log_channel = int(settings.feedback_log_channel)


class GetLatency(commands.Cog):
    def __init__(self, app : commands.Bot) -> None:
        self.app = app
    
    @app_commands.command(name= 'ping', description= "Let's Check Latency!")
    @app_commands.checks.cooldown(3, 150, key= lambda i : (i.guild_id, i.user.id))
    @app_commands.guild_only()
    async def send_latency(self, interaction : Interaction):
        ping = round(self.app.latency * 1000)
        
        original_response_latency = interaction.created_at.now()
        
        await interaction.response.send_message(embed= Embed(
            title= f"<a:loading:1201549182754889759> Bringing a Cookie.....", description= "",
            color= 0x25e173
        ))
        
        
        if interaction.channel.id == log_channel or interaction.channel.id == feedback_log_channel:
            return await not_here_return_embed(interaction= interaction) 
        
        if check_channel_list(interaction= interaction) == False:
            no_permission_embed = get_no_permission_embed()
            return await interaction.response.send_message(embed= no_permission_embed, ephemeral= True, delete_after= 10)

        
        
        if ping >= 0 and ping <= 100 :
            ping_status = "🔵 Very Good"
            embed_latancy = Embed(title= 'ALL LATENCY', description= "You are allowed to use this up to 3 times in 150s.", colour= 0x0074BA)
              
        elif ping > 100 and ping <= 250:
            ping_status = "🟢 Good"
            embed_latancy = Embed(title= 'ALL LATENCY', description= "You are allowed to use this up to 3 times in 150s.", colour= 0x00D26A)
            
        elif ping > 250 and ping <= 500:
            ping_status = "🟡 Not bad"
            embed_latancy = Embed(title= 'ALL LATENCY', description= "You are allowed to use this up to 3 times in 150s.", colour= 0xFCD53F)
            
        elif ping > 500 and ping <= 1000:
            ping_status = "🟠 Bad"
            embed_latancy = Embed(title= 'ALL LATENCY', description= "You are allowed to use this up to 3 times in 150s.", colour= 0xFF6723)
                
        elif ping > 1000:
            ping_status = "🔴 Danger"
            embed_latancy = Embed(title= 'ALL LATENCY', description= "You are allowed to use this up to 3 times in 150s.", colour= 0xF8312F)
                
        
        
        until_latency = await get_datetime()
        latency = ((until_latency - original_response_latency) * 1000).total_seconds()
        
  
        embed_latancy.add_field(name= "API Latency", value= f'{ping}ms\n\n{ping_status}')
        embed_latancy.add_field(name= "Response Latency", value= f'{latency:.0f}ms')
        await interaction.edit_original_response(embed= embed_latancy)
    
    @send_latency.error
    async def srl_error(self, interaction : Interaction, error : app_commands.AppCommandError):
        
        
        if isinstance(error, app_commands.CommandInvokeError):
            pass
    
        
        if isinstance(error, app_commands.CommandOnCooldown):
            embed_cd_error = Embed(title= 'Oops! Please be patient!',
                                           description= f'Retry after {int(error.retry_after)} seconds!',
                                           colour= failed)
            await interaction.response.send_message(embed= embed_cd_error, delete_after=5, ephemeral= True)
            
    

async def setup(app : commands.Bot):
    await app.add_cog(GetLatency(app))