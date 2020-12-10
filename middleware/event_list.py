from uuid import uuid4
import datetime
from data.scraper import IronStarScraper

AVAILABLE_SCRAPERS = [IronStarScraper]
TRIATHLONS = ['OLYMPIC', 'IRONSTAR SUPERMIX', 'SPRINT', 'IRONSTAR 226', 'IRONSTAR 1/4', 'IRONSTAR 1/8', 'IRONSTAR 113']


class TriathlonEvent():
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
        self.is_triathlon: bool = True
        self.short_id: str = str(self.event_id)[0:6]

    def set_properties(self, url: str = None, title: str = None, date: str = None,
                       location: str = None, race_distance: dict = None,
                       image_url: str = None, category: str = None) -> None:
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
        return str(
            f'{self.location} {self.title} {self.date.strftime("%d.%m.%Y")}\n'
            f'{dist_str}\n'
        )

    def populate_event_data(self, event_data: dict) -> None:
        self.set_properties(
            url=event_data['url'],
            title=event_data['title'],
            date=event_data['date'],
            location=event_data['location'],
            image_url=event_data['image_url'],
            race_distance=event_data['race_distance']
        )
        self.is_triathlon = self.title in TRIATHLONS

    def get_short_id(self):
        return self.short_id

    def get_text(self):
        return self.__str__()

    def get_text_with_url(self):
        return self.get_text() + f'{self.url}\n'

    def get_text_with_selector(self):
        return self.get_text() + f'Выбрать эту гонку /race_select_{self.get_short_id()}\n'


class EventList:
    """
    Represents a generic collection of TriathlonEvents
    """

    def __init__(self):
        self.created: datetime.datetime = datetime.datetime.now()
        self.event_list_id: uuid4 = uuid4()
        self.event_list: 'list[TriathlonEvent]' = []
        self.filters: dict = {'is_triathlon': True}
        self.short_id_list: list[str] = []

    def populate_event_list(self) -> None:
        """
        Creates collection of TriathlonEvent objects and populates their properties
        based on web-scraped information
        """
        if self.event_list:  # we don't re-write existing list of events in IronStarEventList object
            return None
        for avail_scraper in AVAILABLE_SCRAPERS:
            scraper = avail_scraper()
            scraper.scrape()
            for event in scraper.get_scrape_data():
                e = TriathlonEvent()
                e.populate_event_data(scraper.parse_single_tag(event))
                self.event_list.append(e)
        # Populate list of short id's and ensure all id's are unique
        self.util_set_short_id_list()
        if not self.util_check_short_ids_unique():
            raise Exception('Got duplicate short_id\'s in EventList instance after populate_event_list')

    # def get_paged_list(self,
    #                    page_size: int,
    #                    print_method: str = None,
    #                    separator: str = '\n',
    #                    lst: 'list[TriathlonEvent]' = None) -> 'list[list[str]]':
    #     """
    #     Returns paged list of TriathlonEvent.__str__'s.
    #     :param page_size: int
    #     :param print_method: one of TriathlonEvent get_text methods. i.e.
    #             get_text - default,
    #             get_text_with_url,
    #             get_text_with_selector
    #     :param separator: Optional = separator between lines within one page of TriathlonEvents
    #     :param lst: Optional = 'list[TriathlonEvent]' to get_paged_list, if not provided - use list from self
    #     This parm exist so that function can print arbitrary list in order to print filtered list
    #     :return: list[list[str]]
    #     """
    #     if not print_method:
    #         print_method = 'get_text'
    #     if not lst:
    #         lst = self.event_list
    #     event_strings = [e.__getattribute__(print_method)() + separator for e in lst]
    #     paged_list = [event_strings[p:p + page_size] for p in range(0, len(event_strings), page_size)]
    #     return paged_list

    def get_paged_list(self,
                       page_size: int,
                       print_method: str = None,
                       separator: str = '\n',
                       lst: 'list[TriathlonEvent]' = None) -> 'list[str]]':
        """
        Returns paged list of TriathlonEvent.__str__'s.
        :param page_size: int
        :param print_method: one of TriathlonEvent get_text methods. i.e.
                get_text - default,
                get_text_with_url,
                get_text_with_selector
        :param separator: Optional = separator between lines within one page of TriathlonEvents
        :param lst: Optional = 'list[TriathlonEvent]' to get_paged_list, if not provided - use list from self
        This parm exist so that function can print arbitrary list in order to print filtered list
        :return: list[list[str]]
        """
        if not print_method:
            print_method = 'get_text'
        if not lst:
            lst = self.event_list
        event_strings = [e.__getattribute__(print_method)() for e in lst]
        paged_list = [separator.join(event_strings[p:p + page_size]) for p in range(0, len(event_strings), page_size)]
        return paged_list

    def filtered_page_print(self, page_size: int, separator: str = '\n', print_method: str = None, ) -> 'list[str]':
        return self.get_paged_list(page_size=page_size,
                                   print_method=print_method,
                                   separator=separator,
                                   lst=self.apply_filters())

    def get_filters(self) -> dict:
        return self.filters

    def update_filters(self, filter_: dict) -> None:
        # todo - reconsider
        # for k, v in filter_.items():
        #     # assert k in TriathlonEvent.__dict__.keys() - todo doesn't work - need another solution
        #     self.filters[k] = v
        self.filters = filter_

    def apply_filters(self) -> 'list[TriathlonEvent]':
        """
        returns filtered (self.filters) list of TriathlonEvents
        todo: Implement date-range filtering
        """

        def helper(x: TriathlonEvent) -> bool:
            result = True
            for k, v in self.filters.items():
                if k in x.__dict__.keys() and not (x.__getattribute__(k) == v):
                    result = False
            return result

        filtered = list(filter(helper, self.event_list))
        return filtered

    def get_short_id_list(self):
        return self.short_id_list

    def util_set_short_id_list(self):
        self.short_id_list = [event.get_short_id() for event in self.event_list]

    def util_check_short_ids_unique(self):
        return len(set(self.short_id_list)) == len(self.short_id_list)
