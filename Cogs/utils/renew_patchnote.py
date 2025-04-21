# 시간 출력 함수
# Last Update : 240130

from bs4 import BeautifulSoup as BS
from discord import Embed
from discord.ext import tasks
from .print_time import get_UTC

import requests


target = 'https://asphaltlegends.com/news/'

@tasks.loop(minutes= 5)
async def get_patchnote_embed():
    
    res = requests.get(target)
    html = res.text
    soup = BS(html, 'html.parser')
    
    if res.status_code == 200:
        
        
        title = soup.find_all(class_ = 'text-h3 pb-4 uppercase')[0].text
        date = soup.find_all(class_ = 'text-lg font-semibold text-dark-blue-500 md:text-xl')[0].text
        summary = soup.find_all(class_ = 'py-4 text-justify text-lg font-semibold md:text-xl')[0].text
        link = soup.find_all('link')[12]['href'][:-3]
        elements = soup.find('div', class_ = 'ck ck-content a6aJuu')
        
        embed = Embed(title= f'**[{date}] {title}**', description= f'제목을 클릭 시 패치노트를 확인하실 수 있습니다!', url= link, colour= 0xFF0055)
        embed.set_author(name= 'ASPHALT 9 : LEGENDS', icon_url= 'https://asphalt9.assets.gameloft.com/assets/a9_logo_12de60294a.png', url= 'https://asphaltlegends.com/')
        embed.set_footer(text= f'{await get_UTC()} (UTC)')
        embed.add_field(name= '< 요약 >', value= f'{summary}\n-----------------------------------', inline= False)
        
            
        if elements:
            
            for tag in elements.children:
                    
                if tag.name == 'ul':
                    for tag_children in tag.children:
                        embed.add_field(name= '', value=f'* {tag_children.get_text(strip = True)}\n', inline= False)
                        
                if tag.name == 'h2' or tag.name == 'h3':
                    embed.add_field(name= f'# {tag.get_text(strip = True)}', value='', inline= False)

        
        return embed
    
    else:
        return None