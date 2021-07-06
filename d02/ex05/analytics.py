from random import randint


class Research:
    def __init__(self, path):
        self.path = path
        self.data = self.file_reader()
        self.calculations = self.Calculations()
        self.analytics = self.Analytics()

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

    class Analytics(Calculations):
        def predict_random(self, num_of_steps):
            dct = {0: [0, 1], 1: [1, 0]}
            return [dct[randint(0, 1)] for x in range(num_of_steps)]

        def predict_last(self, data):
            return data[-1]

        def save_file(self, txt, path, extension='txt'):
            with open(f'{path}.{extension}', 'w') as output_file:
                output_file.write(txt)
