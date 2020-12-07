from data import data_io
from middleware import event_list


def get_event_list(force: bool = False) -> event_list.EventList():
    """
    Reads saved EventList object from pickle (via data_io functions) otherwise
    creates and populates new instance
    :param: force: force to instantiate new EventList object instead of reading from file.
    :return: TriathlonEvent object
    """
    def get_new_event_list_instance():
        obj = event_list.EventList()
        obj.populate_event_list()
        data_io.save_object_to_file(obj)
        return obj

    if force:
        return get_new_event_list_instance()
    else:
        if data_io.pick_newest_file():
            return data_io.load_object_from_file(event_list.EventList, data_io.pick_newest_file())
        return get_new_event_list_instance()
