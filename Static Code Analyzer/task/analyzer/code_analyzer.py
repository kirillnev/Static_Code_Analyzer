import os
import re
import sys


class PEP8:
    MAX_LINE_LEN = 79

    def __init__(self, lines):
        self.line_issues = {}
        self.lines = lines
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
            'S009': {
                'func': self.check_s009,
                'msg': 'Function name function_name should be written in snake_case'
            },
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

    def check_s008(self, line_num):
        line = self.lines[line_num]
        regex_tmpl = r'class +[a-z]'
        return re.match(regex_tmpl, line) is None

    def check_s009(self, line_num):
        line = self.lines[line_num]
        regex_tmpl = r'def +_*[A-Z]'
        return re.match(regex_tmpl, line) is None

    def check_line(self, line_num):
        issues = []
        if len(self.lines[line_num].strip()) > 0:
            for key, value in self.CHECKS.items():
                if not value['func'](line_num):
                    issues.append(key)
        return issues

    def check_lines(self):
        self.line_issues = {i: self.check_line(i) for i in range(len(self.lines))}

    def check_result(self):
        result = []
        for line_num, issues in self.line_issues.items():
            for issue in issues:
                result.append({'line': line_num + 1, 'code': issue, 'msg': self.CHECKS[issue]["msg"]})
        return result

    def __str__(self):
        result = ''
        for line_num, issues in self.line_issues.items():
            for issue in issues:
                result += f'Line {line_num + 1}: {issue} {self.CHECKS[issue]["msg"]}\n'
        return result


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
        result = pep8.check_result()
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


