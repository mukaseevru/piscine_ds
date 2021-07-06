import sys


class Research:
    def __init__(self, path):
        self.path = path
        self.data = self.file_reader()
        self.calculations = self.Calculations()

    def file_reader(self, has_header=True):
        with open(self.path, 'r') as input_file:
            file = input_file.read()
        lines = file.split('\n')
        rest_line = lines
        if has_header:
            first_line = lines[0].split(',')
            if len(first_line) != 2:
                raise Exception('Error in first string')
            rest_line = lines[1:]
        if len(rest_line) == 0:
            raise Exception('There is no data')
        for line in rest_line:
            if line != '0,1' and line != '1,0':
                raise ValueError('Error in strings')
        return [[int(x) for x in line.split(',')] for line in rest_line]

    class Calculations:
        def counts(self, data):
            x = [x[0] for x in data]
            y = [y[1] for y in data]
            return [sum(x), sum(y)]

        def fractions(self, counts):
            return [(counts[0] / (counts[0] + counts[1])) * 100,
                    (counts[1] / (counts[0] + counts[1])) * 100]


if __name__ == '__main__':
    if len(sys.argv) == 2:
        research = Research(sys.argv[1])
        file_reader = research.file_reader()
        print(file_reader)
        counts = research.calculations.counts(file_reader)
        print(counts[0], counts[1])
        fractions = research.calculations.fractions(counts)
        print(fractions[0], fractions[1])
