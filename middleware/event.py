from lxml import html
import requests
from bs4.element import Tag
from bs4 import BeautifulSoup
import re
import uuid
from datetime import datetime


class TriathlonEvent(object):
    """
    Class representing triathlon event including it's Title,
    URL, Image, Distance, Location etc
    """
    def __init__(self, url: str = None, title: str = None, date: str = None, location: str = None,
                 race_distance: dict = None, image_url: str = None):
        """
        Instantiates a TriathlonEvent. All params are optional and set to None by default.
        """
        self.event_id = uuid.uuid4()
        self.url = url
        self.title = title
        self.date = date
        self.location = location
        self.race_distance = race_distance
        self.image_url = image_url

    def set_properties(self, url: str = None, title: str = None, date: str = None, location: str = None,
                       race_distance: dict = None, image_url: str = None) -> None:
        """
        Setter for TriathlonEvent object. All params are optional (None by default).
        Properties are being altered only for those params that not None
        """
        if url:
            self.url = url
        if title:
            self.title = title
        if date:
            self.date = datetime.strptime(date, '%d.%m.%Y')
        if location:
            self.location = location
        if race_distance:
            self.race_distance = race_distance
        if image_url:
            self.image_url = image_url

    def __str__(self) -> str:
        if self.race_distance:
            dist_list = []
            for k, v in self.race_distance.items():
                dist_list.append(k)
                dist_list.append(v)
                dist_list.append('|')
            dist_str = ' '.join(dist_list)
        else:
            dist_str = ''
        return str(f'{self.location} {self.title} {self.date.strftime("%d.%m.%Y")}\n'
                   f'{dist_str}\n'
                   f'{self.url}\n')


class IronStarEvent(TriathlonEvent):
    """
    Class represents IronStart Event.
    Inherits from TriathlonEvent
    """
    base_url = 'https://iron-star.com'
    event_list_url = 'https://iron-star.com/event/'

    def __init__(self):
        super(IronStarEvent, self).__init__()

    def populate_event_data(self, event: Tag) -> None:
        """
        Parses bs4.Element.Tag representing event scraped from https://iron-star.com/event/ list
        and populates IronStarEvent object properties
        :param event: bs4.Element.Tag
        :return: None
        """

        def extract_image_url() -> str:
            """
            Helper: extracts image url from bs4.Tag scraped from https://iron-star.com/event/
            """
            div_url = event.find('div', {'class': 'image'})['style']
            return IronStarEvent.base_url + re.search(r'(\/.*)\);', div_url).group(1)

        def extract_race_distance() -> dict:
            """
            Helper: extracts race distance dict from bs4.Tag scraped from https://iron-star.com/event/
            """
            event_race_distance = {}
            distances = event.find_all('div', {'class': 'triathlon-item'})
            for d in distances:
                tag = str(d.contents[0].contents[0])
                tag = re.search(r'#(.*)\"', tag).group(1)
                text = d.text.strip()
                text = re.search('(\d?(,)?\d*)', text).group(0) + 'km'
                event_race_distance[tag] = text
            return event_race_distance

        self.set_properties(
            url=IronStarEvent.base_url + event.attrs.get('href'),
            title=event.find('div', {'class': 'title'}).get_text().strip(),
            date=event.find('div', {'class': 'date'}).get_text().strip(),
            location=event.find('div', {'class': 'place'}).get_text().strip(),
            image_url=extract_image_url(),
            race_distance=extract_race_distance()
        )


class EventList(object):
    """
    todo class doctring
    """
    def __init__(self):
        self.created = datetime.now()
        self.event_list_id = uuid.uuid4()
        self.event_list: 'list[TriathlonEvent]' = []
        self.filters: 'list[dict]' = []

    def populate_event_list(self):
        pass

    def page_print(self,  page_size: int) -> 'list[list[str]]':
        """
        Returns paged list of TriatlonEvent.__str__'s.
        :param page_size: int
        :return: list[list[str]]
        """
        event_strings = [e.__str__() for e in self.event_list]
        paged_list = [event_strings[p:p + page_size] for p in range(0, len(event_strings), page_size)]
        return paged_list


class IronStarEventList(EventList):
    """
    todo class doctring
    """
    base_url = 'https://iron-star.com'
    event_list_url = 'https://iron-star.com/event/'

    def populate_event_list(self) -> None:
        # todo -> pull this up to base class
        """
        Creates collection of relevant TriathlonEvent objects and populates their properties
        based on web-scraped information
        """
        if self.event_list:  # we don't re-write existing list of events in IronStarEventList object
            return None
        for tag in self.scrape_web():
            i = IronStarEvent()
            i.populate_event_data(tag)
            self.event_list.append(i)

    def scrape_web(self) -> 'list[Tag]':
        """
        Scrapes web site.
        :return: list of events as bs4.element.Tag(s)
        """
        try:
            response = requests.get(self.event_list_url)
            response.raise_for_status()
        except requests.exceptions.HTTPError as ex:
            print(ex.response.text)

        soup = BeautifulSoup(response.content, 'lxml')
        event_bs4_list = []
        # getting list of Tags of all IronStar events
        for tag in soup.find_all('a', {'class': 'event-item'}):
            event_bs4_list.append(tag)
        return event_bs4_list

