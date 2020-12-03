import pickle


def save_object_to_file(obj: object, file_name) -> None:
    with open(file_name, 'wb') as outfile:
        pickle.dump(obj.__dict__, outfile, pickle.HIGHEST_PROTOCOL)


def load_object_from_file(cls, file_name) -> object:
    """
    Unpickles object from file and returns object of a given class
    :param cls: class of an object to return
    :param file_name
    """
    with open(file_name, 'rb') as infile:
        p = pickle.load(infile)
    obj = cls.__new__(cls)
    obj.__dict__.update(p)
    return obj
