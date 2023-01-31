class PEP8:
    MAX_LINE_LEN = 79
    msg = {
        'S001': 'Too long'
    }

    def __init__(self, lines):
        self.issues = {}
        self.lines = lines

    def check_lines_len(self):
        for i in range(len(self.lines)):
            if len(self.lines[i]) > self.MAX_LINE_LEN:
                self. issues[i] = 'S001'

    def __str__(self):
        result = ''
        for line_num, issue in self.issues.items():
            result += f'Line {line_num + 1}: {issue} {self.msg[issue]}\n'
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
        pep8.check_lines_len()
        if len(str(pep8)) > 0:
            print(pep8)


if __name__ == '__main__':
    file_name = input()
    # file_name = '../test/single_line_valid_example.py'

    sca = StaticCodeAnalyzer(file_name)
    sca.run()

