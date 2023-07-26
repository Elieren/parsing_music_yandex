import requests
from bs4 import BeautifulSoup
import numpy as np


class YandexInfoMusic():

    def __init__(self, url):
        self.__url = url
        self.__name = []
        self.__remix = []
        self.__artists = []
        self.__time = []
        self.__full_info = []

    def info(self):
        responce = requests.get(self.__url).text
        soup = BeautifulSoup(responce, 'lxml')
        block = soup.find(
            "div",
            class_='lightlist lightlist_tracks lightlist_clean'
            )
        self.__all_name = block.find_all("div", class_='d-track__name')
        self.__all_artist = block.find_all('div', class_='d-track__meta')
        self.__all_time = block.find_all('div', class_='d-track__end-column')

        self.__selection()
        self.__transformation()

        return self.__full_info, self.__time_array, self.__links, self.__time

    def __selection(self):
        for name in self.__all_name:
            name_track = name.find(
                'a', class_='d-track__title deco-link deco-link_stronger'
                ).get_text(strip=True)
            self.__name.append(name_track)

        for remix in self.__all_name:
            try:
                remix_track = remix.find(
                    'span', class_='d-track__version deco-typo-secondary'
                    ).get_text(strip=True)
                self.__remix.append(remix_track)

            except:
                self.__remix.append(' ')

        for artist in self.__all_artist:
            nick_artist = artist.find(
                'a', class_='deco-link deco-link_muted').get_text(strip=True)
            self.__artists.append(nick_artist)

        for time in self.__all_time:
            time_track = time.find(
                'span', class_='typo-track deco-typo-secondary'
                ).get_text(strip=True)
            time = time_track.replace(':', '.')
            self.__time.append(float(time))

    def __transformation(self):
        i = 0

        info_array = np.column_stack([
            self.__name,
            self.__remix,
            self.__artists
            ])

        while i < len(self.__name):
            complete_data = info_array[i][0] + \
                ' ' + info_array[i][1] + \
                ' ' + info_array[i][2]
            self.__full_info.append(complete_data)
            i += 1

        self.__time_array = [[] for i in range(len(self.__full_info))]
        self.__links = [[] for i in range(len(self.__full_info))]


class HitmotopPars():

    def __init__(self, full_info, time_array, links, time):
        self.__full_info = full_info
        self.__time_array = time_array
        self.__links = links
        self.__time = time
        self.__name = []
        self.__validity_link = []

    def info(self):
        for i, search in enumerate(self.__full_info):
            try:
                url = f'https://rur.hitmotop.com/search?q={search}'

                responce = requests.get(url).text
                soup = BeautifulSoup(responce, 'lxml')

                block = soup.find("div", class_='content-inner')
                all_artist = block.find('ul', class_='tracks__list')
                all_artist = all_artist.find_all('div', class_='track__info-r')

                for artist in all_artist:
                    link = artist.find('a').get('href')
                    self.__links[i].append(link)

                for time in all_artist:
                    time = time.find(
                        'div', class_='track__fulltime').get_text(strip=True)
                    time = time.replace(':', '.')
                    self.__time_array[i].append(float(time))

            except:
                self.__time_array[i].append(0)

        self.__validity()

        return self.__validity_link

    def __validity(self):
        i = 0
        for time in self.__time:
            min_time = time - 0.10
            max_time = time + 0.10

            for x in self.__time_array[0]:
                if x != 0:
                    if i == 0:
                        if (min_time < x) and (x < max_time):
                            self.__validity_link.append(self.__links[0][0])
                            del self.__links[0]
                            del self.__time_array[0]
                            i += 1
                        else:
                            del self.__links[0][0]
                    else:
                        pass
                else:
                    del self.__links[0]
                    del self.__time_array[0]
            i = 0


class Download():

    def __init__(self, full_info, valid_link):
        self.__full_info = full_info
        self.__valid_link = valid_link

    def info(self):

        for i, link in enumerate(self.__valid_link):
            music_bytes = requests.get(link).content
            name = self.__full_info[i]
            print(f"Download: {name}...")
            with open(f'{name}.mp3', 'wb') as file:
                file.write(music_bytes)


url = input("link on playlist: ")

full_info, time_array, links, time = YandexInfoMusic(url).info()

valid_link = HitmotopPars(full_info, time_array, links, time).info()

Download(full_info, valid_link).info()
