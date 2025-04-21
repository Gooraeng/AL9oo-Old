# 로그 채널 경고
# Last Update : 240130

from discord import Interaction, Embed


async def not_here_return_embed(interaction : Interaction):
    not_here_embed = Embed(title= '여기는 로그가 남는 채널입니다', description= f'5초 후에 지워집니다.', colour= 0xfe7866)
    return await interaction.response.send_message(embed= not_here_embed, delete_after= 5)