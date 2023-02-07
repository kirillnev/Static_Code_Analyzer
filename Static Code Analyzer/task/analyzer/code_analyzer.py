import ast
import os
import re
import sys


class PEP8:
    MAX_LINE_LEN = 79

    def __init__(self, lines):
        self.line_issues = []
        self.lines = lines
        self.ast_tree = ast.parse(''.join(lines))
        self.CHECKS = {
            'S001': {
                'func': self.check_s001,
                'msg': 'Too long'
            },
            'S002': {
                'func': self.check_s002,
                'msg': 'Indentation is not a multiple of four'
            },
            'S003': {
                'func': self.check_s003,
                'msg': 'Unnecessary semicolon'
            },
            'S004': {
                'func': self.check_s004,
                'msg': 'At least two spaces required before inline comments'
            },
            'S005': {
                'func': self.check_s005,
                'msg': 'TODO found'
            },
            'S006': {
                'func': self.check_s006,
                'msg': 'More than two blank lines preceding a code line'
            },
            'S007': {
                'func': self.check_s007,
                'msg': 'Too many spaces after construction_name'
            },
            'S008': {
                'func': self.check_s008,
                'msg': 'Class name class_name should be written in CamelCase'
            },
            # 'S009': {
            #     'func': self.check_s009,
            #     'msg': 'Function name function_name should be written in snake_case'
            # },
            # 'S010': {
            #     'func': self.check_s010,
            #     'msg': 'Argument name arg_name should be written in snake_case'
            # },
            # 'S011': {
            #     'func': self.check_s011,
            #     'msg': 'Variable var_name should be written in snake_case'
            # },
            # 'S012': {
            #     'func': self.check_s012,
            #     'msg': 'The default argument value is mutable'
            # },
        }

    def check_s001(self, line_num):
        line = self.lines[line_num]
        return len(line) <= self.MAX_LINE_LEN

    def check_s002(self, line_num):
        line = self.lines[line_num]
        return len(line.lstrip()) == 0 or (len(line) - len(line.lstrip())) % 4 == 0

    def check_s003(self, line_num):
        line = self.lines[line_num]
        return line.split('#')[0].rstrip()[::-1].find(';') != 0

    def check_s004(self, line_num):
        line = self.lines[line_num]
        return line.strip().find('#') <= 0 or line.strip().find('  #') > 0

    def check_s005(self, line_num):
        line = self.lines[line_num]
        return len(line.split('#')) == 1 or line.split('#')[-1].lower().find('todo') == -1

    def check_s006(self, line_num):
        # line = self.lines[line_num]
        return (line_num < 3
                or not (len(self.lines[line_num - 1].strip()) == 0
                        and len(self.lines[line_num - 2].strip()) == 0
                        and len(self.lines[line_num - 3].strip()) == 0))

    def check_s007(self, line_num):
        line = self.lines[line_num]
        regex_tmpl = r' *(?:class|def) {2,}'
        return re.match(regex_tmpl, line) is None

    def is_snake_case(self, name):
        template = r'\b[_a-z0-9]+\b'
        return re.match(template, name) is not None

    def check_s008(self, line_num):
        line = self.lines[line_num]
        regex_tmpl = r'class +[a-z]'
        return re.match(regex_tmpl, line) is None

    def check_s009(self):
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.FunctionDef):
                function_name = node.name
                line_num = node.lineno
                key = 'S009'
                if not self.is_snake_case(function_name):
                    self.line_issues.append({'line': line_num, 'code': key,
                                             'msg': f"Function name '{function_name}' should use snake_case"})


    def check_s010(self):
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.FunctionDef):
                line_num = node.lineno
                key = 'S010'
                for arg in node.args.args:
                    if not self.is_snake_case(arg.arg):
                        self.line_issues.append({'line': line_num, 'code': key,
                                                 'msg': f"Argument name '{arg.arg}' should be written in snake_case"})

    def check_s011(self):
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.FunctionDef):
                line_num = node.lineno
                key = 'S011'
                for node_in_def in node.body:
                    if isinstance(node_in_def, ast.Assign):
                        for target in node_in_def.targets:
                            if hasattr(target, "id"):
                                variable_name = target.id
                                if not self.is_snake_case(variable_name):
                                    self.line_issues.append({'line': line_num + 1, 'code': key,
                                                             'msg': f"Variable '{variable_name}' in function should be snake_case"})

    def check_s012(self):
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.FunctionDef):
                line_num = node.lineno
                key = 'S012'
                for default in node.args.defaults:
                    if not isinstance(default, ast.Constant):
                        self.line_issues.append({'line': line_num, 'code': key,
                                                 'msg': "Default argument value is mutable"})

    def check_line(self, line_num):
        if len(self.lines[line_num].strip()) > 0:
            for key, value in self.CHECKS.items():
                if not value['func'](line_num):
                    self.line_issues.append({'line': line_num + 1, 'code': key, 'msg': self.CHECKS[key]["msg"]})

    def check_lines(self):
        for i in range(len(self.lines)):
            self.check_line(i)


class StaticCodeAnalyzer:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_file(self):
        reading_file = open(self.file_path, 'r')
        file_lines = reading_file.readlines()
        reading_file.close()
        return file_lines

    def run(self):
        pep8 = PEP8(self.read_file())
        pep8.check_lines()
        pep8.check_s009()
        pep8.check_s010()
        pep8.check_s011()
        pep8.check_s012()
        result = pep8.line_issues
        if len(result) > 0:
            for r in result:
                print(f'{self.file_path}: Line {r["line"]}: {r["code"]} {r["msg"]}')


if __name__ == '__main__':
    path = sys.argv[1]
    # print(path)
    if os.path.isdir(path):
        files_name = [path + '/' + fl for fl in os.listdir(path) if fl.endswith('.py')]
    else:
        files_name = [path]
    # print(files_name)
    files_name.sort()
    for fl in files_name:
        # print(fl)
        if fl.endswith('tests.py'):
            continue
        sca = StaticCodeAnalyzer(fl)
        sca.run()


