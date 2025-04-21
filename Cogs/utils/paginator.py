# 디스코드 임베드 페이지 관리자
# Last Update : 240127

from __future__ import annotations
from collections import deque
from discord import ButtonStyle, Embed, Interaction, ui
from typing import List

import asyncio


class Pagination(ui.View):
    def __init__(self,
                 embeds : List[Embed],
                 time_out = 180,
                 _author = None
                 ):
        
        super().__init__(timeout= time_out)
        self._time_out = time_out
        self._author = _author
        self._embeds = embeds
        self._queue = deque(embeds)
        self._initial = embeds[0]
        self._len = len(embeds)
        self._current_page = 1
        self.children[0].disabled = True
        self._queue[0].set_footer(text= f"{self._len} 페이지 중 {self._current_page} 페이지")
    
              
    async def update_buttons(self, interaction : Interaction) -> None:
        for i in self._queue:
            i.set_footer(text= f"{self._len} 페이지 중 {self._current_page} 페이지")
            
        if self._current_page == self._len:
            self.children[2].disabled = True
        else:
            self.children[2].disabled = False

        
        if self._current_page == 1:
            self.children[0].disabled = True
        else:
            self.children[0].disabled = False
            
        
        await interaction.message.edit(view= self)
            
         
    @ui.button(label="<", style= ButtonStyle.primary, row= 0)
    async def previous(self, interaction : Interaction, _):
        self._current_page -= 1
        self._queue.rotate(1)
        embed = self._queue[0]
        await self.update_buttons(interaction = interaction)
        await interaction.response.edit_message(embed= embed)
    
    
    
    @ui.button(label="그만 보기", style= ButtonStyle.danger, row= 0)
    async def delete_message(self, interaction : Interaction, _):
        try:
            await interaction.message.delete()
            self.stop()
            return
        
        except:
            await asyncio.sleep(1)
            await self.delete_message(interaction= interaction)
        
        
        
    @ui.button(label=">", style= ButtonStyle.primary, row= 0)
    async def next(self, interaction : Interaction, _):
        self._queue.rotate(-1)
        embed = self._queue[0]
        self._current_page += 1
        await self.update_buttons(interaction = interaction)
        await interaction.response.edit_message(embed= embed)


    async def on_timeout(self) -> None:
        self.stop()
        
    
    async def interaction_check(self, interaction: Interaction) -> bool:
        if interaction.user == self._author:
            return True
        
        else:
            embed = Embed(title= '저런!', description= '은 조작할 수 없습니다!', color= 0xfe7866)
            await interaction.response.send_message(embed= embed, ephemeral= True, delete_after= 5)
            return False
        
    
    @property
    def initial(self) -> Embed:
        return self._initial
    
