import os
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
                'func': None,
                'msg': 'More than two blank lines preceding a code line'
            }
        }

    def check_s001(self, line):
        return len(line) <= self.MAX_LINE_LEN

    def check_s002(self, line):
        return len(line.lstrip()) == 0 or (len(line) - len(line.lstrip())) % 4 == 0

    def check_s003(self, line):
        return line.split('#')[0].rstrip()[::-1].find(';') != 0

    def check_s004(self, line):
        return line.strip().find('#') <= 0 or line.strip().find('  #') > 0

    def check_s005(self, line):
        return len(line.split('#')) == 1 or line.split('#')[-1].lower().find('todo') == -1

    def check_s006(self, line):
        return True

    def check_line(self, line):
        issues = []
        for key, value in self.CHECKS.items():
            if value['func'] is not None:
                if not value['func'](line):
                    issues.append(key)
        return issues

    def check_lines(self):
        empty_lines = 0
        for i, line in enumerate(self.lines):
            if len(line.strip()) == 0:
                empty_lines += 1
            elif len(self.check_line(line)) > 0:
                self.line_issues[i] = self.check_line(line)
                empty_lines = 0

            if empty_lines > 2 and len(line.strip()) > 0:
                if self.line_issues.get(i) is not None:
                    self.line_issues[i] += ['S006']
                else:
                    self.line_issues[i] = ['S006']
                empty_lines = 0

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


