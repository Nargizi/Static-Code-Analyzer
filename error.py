from typing import List


class Error:
    def __init__(self, code, error_msg, line='', path=''):
        self.code = code
        self.error_msg = error_msg
        self.line = line
        self.path = path

    def __str__(self):
        return f'{self.path}: Line {self.line}: {self.code} {self.error_msg}'


class ErrorLogger:
    def __init__(self, path: str = '',  errors: List[Error] = None):
        if errors is None:
            self.errors = []
        else:
            self.errors = errors
        self.path = path

    def add_error(self, error: Error):
        if self.path != '':
            error.path = self.path
        self.errors.append(error)

    def log(self):
        for error in sorted(self.errors, key=lambda x: (x.path, x.line, x.code, x.error_msg)):
            print(error)

    def clean(self):
        self.errors = []