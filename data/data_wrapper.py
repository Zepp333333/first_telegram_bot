from data import data_io
from middleware import event_list
import datetime


def get_event_list(cls=event_list.IronStarEventList) -> event_list.TriathlonEvent():  # todo - reconsider how we deal with subclasses + type-hint
    if data_io.pick_newest_file():
        return data_io.load_object_from_file(cls, data_io.pick_newest_file())
    else:
        obj = event_list.IronStarEventList()
        obj.populate_event_list()
        data_io.save_object_to_file(obj)
        return obj
