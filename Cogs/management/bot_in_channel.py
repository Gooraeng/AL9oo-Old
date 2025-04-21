# 봇이 채널 리스트에 있는지 체크하는 함수
# Last Update : 240126
from discord.ext import commands
import discord

def check_channel_list(interaction : discord.Interaction) -> bool:
    if interaction.permissions.view_channel == True:
        return True
    
    return False

def get_no_permission_embed():
    embed = discord.Embed(title= '어이쿠!', description= f'무언가 잘못되었습니다. 잠시 후에 다시 시도해주세요.',colour= 0xfe7866)
    embed.add_field(name= '권한 없음', value= '봇의 권한을 다시 확인해주시고 다시 시도해주세요!')
    return embed


        