import re
from error import ErrorLogger, Error

snake_case = re.compile(r'\b[a-z_\d]+\b')
camel_case = re.compile(r'\b[A-Z]([a-z]+[A-Z]?)*\b')


def is_func(line):
    return re.search(r'\bdef\b', line) is not None


def is_class(line):
    return re.search(r'\bclass\b', line) is not None


def is_snake_case(string):
    return snake_case.match(string) is not None


def is_camel_case(string):
    return camel_case.match(string) is not None


def check_error(line, num_line, logger: ErrorLogger):
    if is_func(line):
        if re.search(r'\bdef \S', line) is None:
            logger.add_error(Error('S007',
                                   'Too many spaces after construction_name (def or class)',
                                   num_line))
    elif is_class(line):
        if re.search(r'\bclass \S', line) is None:
            logger.add_error(Error('S007',
                                   'Too many spaces after construction_name (def or class)',
                                   num_line))
