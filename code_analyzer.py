import os
import sys
from regex_matcher import check_error as check_regex_error
from error import Error, ErrorLogger
from ast_analyzer import ast_analyze

MAX_LINE_LENGTH = 79
logger = ErrorLogger()


def check_error(cond, num_line, code, msg):
    if cond:
        logger.add_error(Error(code, msg, num_line))


def is_blank_line(line):
    if len(line.strip()) == 0:
        return True
    return False


def check_code_line_errors(code_line, num_line):
    check_error(not is_blank_line(code_line) and len(code_line) - len(code_line.rstrip(' ')) < 2,
                num_line, 'S004', 'Less than two spaces before inline comments')


def check_comment_line_errors(comment_line, num_line):
    check_error('TODO' in comment_line.upper(),
                num_line, 'S005', 'TODO found')


def check_one_line_errors(line, num_line):
    check_regex_error(line, num_line, logger)

    check_error(len(line.rstrip()) > MAX_LINE_LENGTH,
                num_line, 'S001', 'Too Long')

    check_error((len(line) - len(line.lstrip(' '))) % 4 != 0,
                num_line, 'S002', 'Indentation is not a multiple of four')

    try:
        code_end = line.index('#')
    except ValueError:
        code_end = len(line)
    else:
        code_line = line[:code_end]  # part of the code before inline comment
        comment_line = line[code_end + 1:]
        check_code_line_errors(code_line, num_line)
        check_comment_line_errors(comment_line, num_line)
    finally:
        check_error(len(line[:code_end].rstrip()) != 0 and line[:code_end].rstrip()[-1] == ';',
                    num_line, 'S003', 'Unnecessary semicolon after a statement')


def analyze_file(file_):
    blank_count = 0

    for num_line, line in enumerate(file_, start=1):
        # multi-line checks
        if is_blank_line(line):
            blank_count += 1
            continue
        else:
            check_error(blank_count > 2,
                        num_line, 'S006', 'More than two blank lines preceding a code line ')
            blank_count = 0

        check_one_line_errors(line, num_line)


def get_path():
    args = sys.argv
    try:
        path = args[1]
    except IndexError:
        print('You must specify file or directory')
    else:
        return path


def get_files(path):
    files = []
    if os.path.isfile(path):
        files.append(path)
    else:
        with os.scandir(path) as entries:
            for entry in entries:
                if entry.is_file() and entry.name.endswith('.py'):
                    files.append(os.path.join(path, entry.name))
    return files


if __name__ == '__main__':
    dir_path = get_path()
    py_files = get_files(dir_path)
    for file_path in sorted(py_files):
        with open(file_path) as file:
            logger.clean()
            logger.path = file_path
            analyze_file(file)

        with open(file_path) as file:
            ast_analyze(file, logger)
        logger.log()