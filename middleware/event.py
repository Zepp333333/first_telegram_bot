from lxml import html
import requests
from bs4 import BeautifulSoup
import re
import uuid


class TriathlonEvent(object):
    """
    Class representing triathlon event including their Title,
    URL, Image, Distance, Location etc
    """
    def __init__(self):
        self.event_id = uuid.uuid4()
        self.url = None
        self.title = None
        self.date = None
        self.location = None
        self.race_distance = None
        self.image_url = None

    def add_data(self, url=None, title=None, date=None, location=None, race_distance=None, image_url=None):
        if url:
            self.url = url
        if title:
            self.title = title
        if date:
            self.date = date
        if location:
            self.location = location
        if race_distance:
            self.race_distance = race_distance
        if image_url:
            self.image_url = image_url

    def __str__(self):
        return


class IronStartEvent(TriathlonEvent):
    ironstar_base_url = 'https://iron-star.com'
    ironstar_event_list_url = 'https://iron-star.com/event/'

    def __init__(self):
        super(IronStartEvent, self).__init__()

    def pupulate_event_data(self, event):
        self.add_data(
            url=IronStartEvent.ironstar_base_url + event.attrs.get('href'),
            title=event.find('div', {'class': 'title'}).get_text().strip(),
            date=event.find('div', {'class': 'date'}).get_text().strip(),
            location=event.find('div', {'class': 'place'}).get_text().strip(),
        )

        # making-up image url
        # todo extract method/function
        div_url = event.find('div', {'class': 'image'})['style']
        image_url = IronStartEvent.ironstar_base_url + re.search(r'(\/.*)\);', div_url).group(1)
        self.add_data(image_url=image_url)

        # making-up distances
        # todo extract method/function
        event_race_distance = {}
        distances = event.find_all('div', {'class': 'triathlon-item'})
        for distance in distances:
            tag = str(distance.contents[0].contents[0])
            tag = re.search(r'#(.*)\"', tag).group(1)

            text = distance.text.strip()
            text = re.search('(\d*)', text).group(0) + 'km'

            event_race_distance[tag] = text
        self.add_data(race_distance=event_race_distance)

    def __str__(self):
        if self.race_distance:
            distance = []
            for k, v in self.race_distance.items():
                distance.append(k)
                distance.append(v)
                distance.append('|')
            distance = ' '.join(distance)


        return str(f'{self.location} {self.title} {self.date}\n'
                   f'{distance}\n'
                   f'{self.url}\n')


ironstar_event_list_url = 'https://iron-star.com/event/'
response = requests.get(ironstar_event_list_url)
html = response.content
#
soup = BeautifulSoup(html, 'lxml')
event_list = []
# getting list of all IronStar events
for event in soup.find_all('a', {'class':'event-item'}):
    event_list.append(event)

# example event
# event = event_list[-1]
all_events = []
for event in event_list:
    i = IronStartEvent()
    i.pupulate_event_data(event)
    all_events.append(i)


