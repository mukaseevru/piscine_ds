import sys


class Research:
    def __init__(self, path):
        self.path = path

    def file_reader(self):
        with open(self.path, 'r') as input_file:
            file = input_file.read()
        lines = file.split('\n')
        first_line = lines[0].split(',')
        if len(first_line) != 2:
            raise Exception('Error in first string')
        rest_line = lines[1:]
        if len(rest_line) == 0:
            raise Exception('There is no data')
        for line in rest_line:
            if line != '0,1' and line != '1,0':
                raise ValueError('Error in strings')
        return file


if __name__ == '__main__':
    if len(sys.argv) == 2:
        research = Research(sys.argv[1])
        print(research.file_reader())
