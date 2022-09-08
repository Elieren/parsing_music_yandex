import requests
from bs4 import BeautifulSoup
import lxml
import os
import platform
import re
import numpy as np


name_list = []
remix_list = []
artist_list = []
time_list = []
timer = []
link = []
stat = []
nnam = []

full = []

lop = 0
law = 0

url = input("link: ")

responce = requests.get(url).text
soup = BeautifulSoup(responce, 'lxml')
block = soup.find("div", class_='lightlist lightlist_tracks lightlist_clean')
all_name = block.find_all("div", class_='d-track__name')
all_artist = block.find_all('div', class_='d-track__meta')
all_time = block.find_all('div', class_='d-track__end-column')


for name in all_name:
    name_track = name.find(
        'a', class_='d-track__title deco-link deco-link_stronger').get_text(strip=True)
    name_list.append(name_track)

for remix in all_name:
    try:
        remix_track = remix.find(
            'span', class_='d-track__version deco-typo-secondary').get_text(strip=True)
        remix_list.append(remix_track)

    except:
        remix_list.append(' ')

for artist in all_artist:
    nick_artist = artist.find(
        'a', class_='deco-link deco-link_muted').get_text(strip=True)
    artist_list.append(nick_artist)

for time in all_time:
    time_track = time.find(
        'span', class_='typo-track deco-typo-secondary').get_text(strip=True)
    p = time_track.replace(':', '.')
    p = float(p)
    time_list.append(p)

kol_vo = len(name_list)

lister = np.column_stack([name_list, remix_list, artist_list])

while lop < kol_vo:
    l = lister[lop][0] + ' ' + lister[lop][1] + ' ' + lister[lop][2]
    lop += 1
    full.append(l)

rac = len(full)
timer = [[] for i in range(rac)]

link = [[] for i in range(rac)]

for search in full:
    try:
        url = f'https://ru.hitmotop.com/search?q={search}'

        responce = requests.get(url).text
        soup = BeautifulSoup(responce, 'lxml')

        block = soup.find("div", class_='content-inner')
        all_artist = block.find('ul', class_='tracks__list')
        lop = all_artist.find_all('div', class_='track__info-r')

        for artist in lop:
            image_link = artist.find('a').get('href')
            link[law].append(image_link)


        for time in lop:
            time_a = time.find(
                'div', class_='track__fulltime').get_text(strip=True)
            k = time_a.replace(':', '.')
            k = float(k)
            timer[law].append(k)
        
        nnam.append(search)
    except:
        timer[law].append(0)
    law += 1

lor = 0
for ti in time_list:
    min_time = ti - 0.10
    max_time = ti + 0.10

    for x in timer[0]:
        if x != 0:
            if lor == 0:
                if (min_time < x) and (x < max_time):
                    stat.append(link[0][0])
                    del link[0]
                    del timer[0]
                    lor += 1
                else:
                    del link[0][0]
            else:
                pass
        else:
            del link[0]
            del timer[0]
    lor = 0

po = 0

for link in stat:
    music_bytes = requests.get(link).content
    lopl = nnam[po]
    print(f"Download: {lopl}...")
    with open(f'{lopl}.mp3', 'wb') as file:
        file.write(music_bytes)
    po += 1
