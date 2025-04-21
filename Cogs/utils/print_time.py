# 시간 출력 함수
# Last Update : 240130

from discord.ext import tasks
from datetime import datetime

import urllib.request


month = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06', \
    'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}
url = 'https://time.navyism.com/'


# 1초마다 시간 집계
@tasks.loop(seconds=1)
async def get_UTC():
    date = urllib.request.urlopen(url).headers['Date'][5:-4]
    d, m, y, hour, min, sec = date[:2], month[date[3:6]], date[7:11], date[12:14], date[15:17], date[18:]

    return f'{y}-{m}-{d} > {hour}:{min}:{sec}'


@tasks.loop(seconds= 0.001)
async def get_datetime():
    return datetime.now()