import pickle
import datetime
import os
from data.config import (
    DEFAULT_DATA_DIR,
    DEFAULT_OBJECT_FILE_EXT,
    DEFAULT_EVENT_LIST_FILE_NAME_BASE,
)


def save_object_to_file(obj: object, file_name: str = None, dir_: str = DEFAULT_DATA_DIR) -> None:
    if not file_name:
        file_name = DEFAULT_EVENT_LIST_FILE_NAME_BASE + \
                    datetime.datetime.now().strftime('%d-%m-%Y-%H-%M-%S') + \
                    DEFAULT_OBJECT_FILE_EXT
    with open(dir_ + file_name, 'wb') as outfile:
        pickle.dump(obj.__dict__, outfile, pickle.HIGHEST_PROTOCOL)


def load_object_from_file(cls: object, file_name: str, dir_: str = DEFAULT_DATA_DIR) -> object:
    """
    Unpickles object from file and returns object of a given class
    :param cls: class of an object to return
    :param file_name
    :param dir_: directory
    """
    with open(dir_ + file_name, 'rb') as infile:
        p = pickle.load(infile)
    obj = cls.__new__(cls)
    obj.__dict__.update(p)
    return obj


def pick_newest_file(dir_: str = DEFAULT_DATA_DIR, file_type: str = DEFAULT_OBJECT_FILE_EXT) -> str:
    def get_saved_event_list_objects() -> list:
        return [f for f in os.listdir(dir_) if f.endswith(file_type)]

    def get_file_modification_date(file_name: str) -> datetime.datetime:
        t = os.path.getmtime(dir_ + file_name)
        return datetime.datetime.fromtimestamp(t)

    dates_files = {get_file_modification_date(f): f for f in get_saved_event_list_objects()}
    return dates_files[sorted(dates_files)[-1]] if dates_files else ''
