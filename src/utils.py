import os
import random
import yaml
from datetime import datetime, timezone
from jinja2 import Environment, FileSystemLoader, select_autoescape


def load_template(template_folder: str = 'templates') -> Environment:
    """Load Jinja2 environment with the specified template folder.

    Args:
        template_folder (str): The folder containing the templates. Defaults to 'templates'.

    Returns:
        Environment: The Jinja2 environment.
    """
    env = Environment(
        loader=FileSystemLoader(template_folder),
        autoescape=select_autoescape()
    )
    return env


def parse_yaml(folder: str, file: str) -> dict:
    """Parse a YAML file and return its contents as a dictionary.

    Args:
        folder (str): The folder containing the YAML file.
        file (str): The name of the YAML file.

    Returns:
        dict: The parsed YAML content.
    """
    reader = read_file(folder, file)
    config = yaml.safe_load(reader)
    return config


def read_file(folder: str, filename: str) -> str:
    """Read the contents of a file and return it as a string.

    Args:
        folder (str): The folder containing the file.
        filename (str): The name of the file.

    Returns:
        str: The contents of the file.
    """
    with open(os.path.join(folder, filename), 'r') as f:
        return f.read()


def filter_dict(data: dict, filter_key: list) -> dict:
    """Filter a dictionary by a list of keys.

    Args:
        data (dict): The dictionary to filter.
        filter_key (list): The list of keys to keep in the dictionary.

    Returns:
        dict: The filtered dictionary.
    """
    return { k: v for k,v in data.items() if k in filter_key }


def rename_keys(dictionary: dict, mapping: dict) -> dict:
    """Rename keys in a dictionary based on a mapping.

    Args:
        dictionary (dict): The dictionary with keys to rename.
        mapping (dict): A dictionary mapping old keys to new keys.

    Returns:
        dict: The dictionary with renamed keys.
    """
    for old_key in mapping:
        new_key = mapping[old_key]
        dictionary[new_key] = dictionary.pop(old_key)
    return dictionary


def random_int(start: int, end: int) -> int:
    """Generate a random integer between start and end, inclusive.

    Args:
        start (int): The lower bound of the random integer.
        end (int): The upper bound of the random integer.

    Returns:
        int: The generated random integer.
    """
    min = end
    for _ in range(start+2):
        result = random.randint(start, end)
        if min >= result:
            min = result
    return min


def get_current_str_datetime():
    """Get the current datetime in string format.
    """
    return datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')


def get_current_datetime():
    """Get the current datetime.
    """
    return datetime.now(timezone.utc)


def parse_variable(var: str | datetime) -> str:
    """Parse a variable to a string if it is a datetime object.

    Args:
        var (str | datetime): The variable to parse.
    Returns:
        str: The parsed variable.
    """
    if isinstance(var, datetime):
        return var.strftime('%Y-%m-%d %H:%M:%S')
    else:
        return var
