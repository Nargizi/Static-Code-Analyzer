import ast
import itertools
from error import ErrorLogger, Error
from regex_matcher import is_snake_case, is_camel_case


class Analyzer(ast.NodeVisitor):
    def __init__(self, logger: ErrorLogger):
        self.logger = logger


class Analyzer(Analyzer):
    def visit_FunctionDef(self, node):
        if not is_snake_case(node.name):
            self.logger.add_error(Error('S009',
                                        'Function name function_name should be written in snake_case',
                                        node.lineno))

        for arg in node.args.args:
            if not is_snake_case(arg.arg):
                self.logger.add_error(Error('S010',
                                            'Argument name arg_name should be written in snake_case;',
                                            node.lineno))

        for default in itertools.chain(node.args.defaults, node.args.kw_defaults):
            if default is None:
                continue
            if isinstance(default, (ast.Dict, ast.Set, ast.List)):
                self.logger.add_error(Error('S012',
                                            'The default argument value is mutable.',
                                            node.lineno))
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        if not is_camel_case(node.name):
            self.logger.add_error(Error('S008',
                                        'Class name class_name should be written in CamelCase',
                                        node.lineno))
        self.generic_visit(node)

    def visit_Assign(self, node):
        for var in node.targets:
            if isinstance(var, ast.Name):
                if not is_snake_case(var.id):
                    self.logger.add_error(Error('S011',
                                                'Variable var_name should be written in snake_case;',
                                                node.lineno))


def ast_analyze(file, logger):
    tree = ast.parse(file.read())
    Analyzer(logger).visit(tree)
