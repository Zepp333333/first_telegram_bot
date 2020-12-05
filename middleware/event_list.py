from uuid import uuid4
import datetime
from data.scraper import IronStarScraper


class TriathlonEvent(object):
    """
    Class representing triathlon event including it's Title,
    URL, Image, Distance, Location etc
    """

    def __init__(self):
        self.event_id: uuid4 = uuid4()
        self.url: str = ''
        self.title: str = ''
        self.date: datetime.datetime = datetime.datetime.fromtimestamp(datetime.MINYEAR)
        self.location: str = ''
        self.race_distance: dict = {}
        self.image_url: str = ''

    def set_properties(self, url: str = None, title: str = None, date: str = None,
                       location: str = None, race_distance: dict = None,
                       image_url: str = None) -> None:
        """
        Setter for TriathlonEvent object. All params are optional (None by default).
        Properties are being altered only for those params that not None
        """
        if url:
            self.url = url
        if title:
            self.title = title
        if date:
            self.date = datetime.datetime.strptime(date, '%d.%m.%Y')
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

    def populate_event_data(self, event_data: dict) -> None:
        self.set_properties(
            url=event_data['url'],
            title=event_data['title'],
            date=event_data['date'],
            location=event_data['location'],
            image_url=event_data['image_url'],
            race_distance=event_data['race_distance']
        )


class IronStarEvent(TriathlonEvent):
    pass


class IronManEvent(TriathlonEvent):
    pass


class EventList(object):
    """
    Represents a generic collection of TriathlonEvents
    """

    def __init__(self):
        self.created: datetime.datetime = datetime.datetime.now()
        self.event_list_id: uuid4 = uuid4()
        self.event_list: 'list[TriathlonEvent]' = []
        self.filters: dict = {}

    def populate_event_list(self, event_cls) -> None:
        """
        Creates collection of relevant TriathlonEvent objects and populates their properties
        based on web-scraped information
        """
        if self.event_list:  # we don't re-write existing list of events in IronStarEventList object
            return None
        # check which event class we use
        if event_cls == IronStarEvent:
            scraper = IronStarScraper()
            scraper.scrape()
        elif event_cls == IronManEvent:
            raise Exception('Not Implemented: IronManEvent')  # todo : Implement

        for event in scraper.get_scrape_data():
            e = TriathlonEvent()
            e.populate_event_data(scraper.parse(event))
            self.event_list.append(e)

    def page_print(self, page_size: int, lst: 'list[TriathlonEvent]' = None) -> 'list[list[str]]':
        """
        Returns paged list of TriatlonEvent.__str__'s.
        :param lst: Optional = 'list[TriathlonEvent]' to page_print, if not provided - use list from self
        This parm exist so that function can print arbitrary list in order to print filtered list
        :param page_size: int
        :return: list[list[str]]
        """
        if not lst:
            lst = self.event_list
        event_strings = [e.__str__() for e in lst]
        paged_list = [event_strings[p:p + page_size] for p in range(0, len(event_strings), page_size)]
        return paged_list

    def filtered_page_print(self, page_size: int) -> 'list[list[str]]':
        return self.page_print(page_size, self.apply_filters())

    def get_filters(self) -> dict:
        return self.filters

    def update_filters(self, filter_: dict) -> None:
        for k, v in filter_.items():
            # assert k in TriathlonEvent.__dict__.keys() - todo doesn't work - need another solution
            self.filters[k] = v

    def apply_filters(self) -> 'list[TriathlonEvent]':
        """
        returns filtered (self.filters) list of TriathlonEvents
        todo: Implement date-range filtering
        """

        def helper(x: TriathlonEvent) -> bool:
            result = True
            for k, v in self.filters.items():
                if k in x.__dict__.keys() and not (x.__getattribute__(k).lower() == v.lower()):
                    result = False
            return result

        filtered = list(filter(helper, self.event_list))
        return filtered


# todo - remove
# test code
# import pickle
# el = EventList()
# el.populate_event_list(IronStarEvent)
# el.update_filters({'location': 'Сочи'})
# save_object_to_file(i_list, 'dump.p')
# irr = load_object_from_file(IronStarEventList, 'dump.p')
