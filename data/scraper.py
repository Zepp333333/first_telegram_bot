from requests import get, exceptions
from bs4.element import Tag
from bs4 import BeautifulSoup
from data import config
import re


class IronStarScraper(object):
    def __init__(self, url: str = config.IRONSTAR_EVENT_LIST_URL):
        self.url = url
        self.scrape_data: 'list[Tag]' = []
        self.parsed_data: dict = {}
        self.pasrsing_keys: list = [
            'url',
            'title',
            'date',
            'location',
            'race_distance',
            'image_url'
        ]

    def get_scrape_data(self):
        return self.scrape_data

    def scrape(self) -> None:
        """
        Scrapes web site.
        :return: list of events as bs4.element.Tag(s)
        """
        try:
            response = get(self.url)
            response.raise_for_status()
        except exceptions.HTTPError as ex:
            raise Exception(ex.response.text)

        soup = BeautifulSoup(response.content, 'lxml')
        event_bs4_list = []
        # getting list of Tags of all IronStar events
        for tag in soup.find_all('a', {'class': 'event-item'}):
            event_bs4_list.append(tag)
        self.scrape_data = event_bs4_list

    def parse(self, tag) -> dict:
        for key in self.pasrsing_keys:
            fn = 'extract_' + key
            self.parsed_data[key] = self.__getattribute__(fn)(tag)
        return self.parsed_data

    @staticmethod
    def extract_image_url(tag: Tag) -> str:
        """
        Helper: extracts image url from bs4.Tag scraped from https://iron-star.com/event/
        """
        div_url = tag.find('div', {'class': 'image'})['style']
        return config.IRONSTAR_BASE_URL + re.search(r'(/.*)\);', div_url).group(1)

    @staticmethod
    def extract_race_distance(tag: Tag) -> dict:
        """
        Helper: extracts race distance dict from bs4.Tag scraped from https://iron-star.com/event/
        """
        event_race_distance = {}
        distances = tag.find_all('div', {'class': 'triathlon-item'})
        for d in distances:
            key = str(d.contents[0].contents[0])
            key = re.search(r'#(.*)\"', key).group(1)
            value = d.text.strip()
            value = re.search('(\d?(,)?\d*)', value).group(0) + 'km'
            event_race_distance[key] = value
        return event_race_distance

    @staticmethod
    def extract_url(tag: Tag) -> str:
        return config.IRONSTAR_BASE_URL + tag.attrs.get('href')

    @staticmethod
    def extract_title(tag: Tag) -> str:
        return tag.find('div', {'class': 'title'}).get_text().strip()

    @staticmethod
    def extract_date(tag: Tag) -> str:
        return tag.find('div', {'class': 'date'}).get_text().strip()

    @staticmethod
    def extract_location(tag: Tag) -> str:
        return tag.find('div', {'class': 'place'}).get_text().strip()
