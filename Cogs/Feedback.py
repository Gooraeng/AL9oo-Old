# 피드백 요청을 남기는 명령어
# Last Update : 240130

from discord import app_commands, ButtonStyle, Embed, Interaction, TextStyle, ui
from discord.ext import commands
from .management.bot_in_channel import check_channel_list, get_no_permission_embed
from .utils import print_time, settings
from .utils.embed_log import succeed, failed, etc, interaction_with_server
from .utils.not_here import not_here_return_embed


feedback_log_channel = int(settings.feedback_log_channel)
log_channel = int(settings.log_channel)


# 명령어 함수 
class Feedback(commands.Cog):
    def __init__(self, app : commands.Bot) :
        self.app = app

         
    @app_commands.command(name= '피드백', description= '뭔가 피드백을 남기고 싶은 게 있나요?')
    @app_commands.checks.cooldown(1, 30, key= lambda i :(i.guild_id, i.user.id))
    @app_commands.guild_only()
    async def warn_spawnmodal(self, interaction : Interaction):
        
        if interaction.channel.id == log_channel or interaction.channel.id == feedback_log_channel:
            return await not_here_return_embed(interaction= interaction)
        
        if check_channel_list(interaction= interaction) == False:
            no_permission_embed = get_no_permission_embed()
            return await interaction.response.send_message(embed= no_permission_embed, ephemeral= True, delete_after= 10)           
           
            
        embed_warn = Embed(title= '❗경고', description= '문제 전송 시 중간에 취소할 수 없습니다!', colour= interaction_with_server)
        embed_warn.add_field(name= '', value= '이 명령어를 실행하실 때 마다 30초의 쿨타임이 존재합니다!', inline= False)
        embed_warn.add_field(name= '', value= '숙지하셨다면 어떤 문제를 신고하실 것인지 버튼을 눌러 진행해주십시오.', inline= False)
        await interaction.response.send_message('', embed= embed_warn, view= warn_before(), ephemeral= True)
            
 
          
    @warn_spawnmodal.error
    async def cooldown_err(self, interaction : Interaction, error : app_commands.AppCommandError):
        
        if isinstance(error, app_commands.CommandOnCooldown):
            
            embed_cd_error = Embed(title= '어이쿠! 아직 이용하실 수 없습니다!',
                                           description= f'{int(error.retry_after)}초 후에 다시 시도해주세요!',
                                           colour= failed)
            await interaction.response.send_message(embed= embed_cd_error, delete_after=5, ephemeral= True)
        



class FixModal(ui.Modal, title = '데이터 수정 요청'):    
        
    fix_problem = ui.TextInput(
        label= '세부 설명(필수)',
        style= TextStyle.long,
        placeholder= '문제를 자세히 적어주세요!',
        max_length= 1000,
        required= True,
    )
    
    async def on_submit(self, interaction: Interaction) -> None:
        feedback_ch = interaction.client.get_channel(feedback_log_channel)
        
        embed_sent = Embed(title= '전송 완료', description= '정상적으로 전송이 완료되었습니다!', colour= succeed)
        await interaction.response.send_message(embed= embed_sent, ephemeral= True, delete_after= 10)
        
        embed_problem = Embed(title= 'Feedback 추가', description= '데이터 수정 요청', colour= 0x09f000)
        embed_problem.add_field(name= '시간 (UTC)', value= f'{await print_time.get_UTC()}', inline= True)
        embed_problem.add_field(name= '서버명 (ID)', value= f'{interaction.guild.name} ({interaction.guild.id})', inline= True)
        embed_problem.add_field(name= '유저명 (Global)', value= f'{interaction.user.global_name}')
        embed_problem.add_field(name= '문제 묘사', value= self.fix_problem.value, inline= False)
        
        await feedback_ch.send(embed= embed_problem)
        
    
    
class SuggestModal(ui.Modal, title= '기타 제안'):    
    
    suggest = ui.TextInput(
        label= '세부 설명(필수)',
        style= TextStyle.long,
        placeholder= '자세히 적어주세요!',
        max_length= 1000,
        required= True,
    )
    
    async def on_submit(self, interaction: Interaction) -> None:
        feedback_ch = interaction.client.get_channel(feedback_log_channel)
        
        embed_sent = Embed(title= '전송 완료', description= '정상적으로 전송이 완료되었습니다!', colour= succeed)
        await interaction.response.send_message(embed= embed_sent, ephemeral= True, delete_after= 10)
        
        embed_problem = Embed(title= 'Feedback 추가', description= '기타 제안', colour= 0x0407f9)
        embed_problem.add_field(name= '시간 (UTC)', value= f'{await print_time.get_UTC()}', inline= True)
        embed_problem.add_field(name= '서버명 (ID)', value= f'{interaction.guild.name} ({interaction.guild.id})', inline= True)
        embed_problem.add_field(name= '유저명 (Global)', value= f'{interaction.user.global_name}')
        embed_problem.add_field(name= '문제 묘사', value= self.suggest.value, inline= False)
        await feedback_ch.send(embed= embed_problem)
        
             
        
class ReportModal(ui.Modal, title = '봇 작동 신고'):    
            
    problem = ui.TextInput(
        label= '세부 설명(필수)',
        style= TextStyle.long,
        placeholder= '문제를 자세히 적어주세요!',
        max_length= 1000,
        required= True,
    )
    
    async def on_submit(self, interaction: Interaction) -> None:
        feedback_ch = interaction.client.get_channel(feedback_log_channel)
        gooraeng = interaction.client.get_user(303915314062557185)
        
        embed_sent = Embed(title= '전송 완료', description= '정상적으로 전송이 완료되었습니다!', colour= succeed)
        await interaction.response.send_message(embed= embed_sent, ephemeral= True, delete_after= 10)
        
        embed_problem = Embed(title= '봇 작동 신고', description= 'Report', colour= 0xf50500)
        embed_problem.add_field(name= '시간 (UTC)', value= f'{await print_time.get_UTC()}', inline= True)
        embed_problem.add_field(name= '서버명 (ID)', value= f'{interaction.guild.name} ({interaction.guild.id})', inline= True)
        embed_problem.add_field(name= '유저명 (Global)', value= f'{interaction.user.global_name}')
        embed_problem.add_field(name= '세부 설명', value= self.problem.value, inline= False)
        
        
        await feedback_ch.send(f'{gooraeng.mention}', embed= embed_problem)
        
        
        
class warn_before(ui.View):
    def __init__(self):
        super().__init__(timeout= None)
        self.cooldown = commands.CooldownMapping.from_cooldown(1, 30, commands.BucketType.member)
        
        
    @ui.button(label= '봇 작동 신고', style= ButtonStyle.danger)
    async def report_prob(self, interaction : Interaction, button : ui.Button):
        
        interaction.message.author = interaction.user
        bucket = self.cooldown.get_bucket(interaction.message)
        retry = bucket.update_rate_limit()
        
        if retry == None:
            await interaction.response.send_modal(ReportModal())
        
        else:
            embed_cd_error = Embed(title= '버튼을 마구 누르시면 안 됩니다!', description= f'{round(retry, 1)}초 후에 다시 시도해주세요!', colour= failed)
            await interaction.response.send_message(embed= embed_cd_error, ephemeral= True, delete_after= 5)
          
        
    @ui.button(label= '데이터 수정 요청', style= ButtonStyle.green)
    async def request_fix(self, interaction : Interaction, button : ui.Button):
        
        interaction.message.author = interaction.user
        bucket = self.cooldown.get_bucket(interaction.message)
        retry = bucket.update_rate_limit()
        
        if retry == None:
            await interaction.response.send_modal(FixModal())
        
        else:
            embed_cd_error = Embed(title= '버튼을 마구 누르시면 안 됩니다!', description= f'{round(retry, 1)}초 후에 다시 시도해주세요!', colour= failed)
            await interaction.response.send_message(embed= embed_cd_error, ephemeral= True, delete_after= 5)
        
        
    
    @ui.button(label= '기타 제안', style= ButtonStyle.primary)
    async def suggestion(self, interaction : Interaction, button : ui.Button):
        
        interaction.message.author = interaction.user
        bucket = self.cooldown.get_bucket(interaction.message)
        retry = bucket.update_rate_limit()
        
        if retry == None:
            await interaction.response.send_modal(SuggestModal())
        
        else:
            embed_cd_error = Embed(title= '버튼을 마구 누르시면 안 됩니다!', description= f'{round(retry, 1)}초 후에 다시 시도해주세요!', colour= failed)
            await interaction.response.send_message(embed= embed_cd_error, ephemeral= True, delete_after= 5)
 
                          
async def setup(app : commands.Bot):
    await app.add_cog(Feedback(app))