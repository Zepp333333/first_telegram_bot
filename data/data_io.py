import pickle
import datetime
import os

# todo: move to config
DEFAULT_DATA_DIR = './'  # todo change to 'data/'
DEFAULT_OBJECT_FILE_EXT = '.p'
DEFAULT_FILE_NAME_BASE = 'ironstar_'


def save_object_to_file(obj: object, file_name: str = None, dir_: str = DEFAULT_DATA_DIR) -> None:
    if not file_name:
        file_name = DEFAULT_FILE_NAME_BASE + datetime.datetime.now().strftime('%d-%m-%Y') + DEFAULT_OBJECT_FILE_EXT
    with open(file_name, 'wb') as outfile:
        pickle.dump(obj.__dict__, outfile, pickle.HIGHEST_PROTOCOL)


def load_object_from_file(cls: object, file_name: str, dir_: str = DEFAULT_DATA_DIR) -> object: # todo need type-hint for cls
    """
    Unpickles object from file and returns object of a given class
    :param cls: class of an object to return
    :param file_name
    :param dir_: directory
    """
    with open(file_name, 'rb') as infile:
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

    dates_files = {get_file_modification_date(dir_): f for f in get_saved_event_list_objects()}
    return dates_files[sorted(dates_files)[-1]] if dates_files else ''
