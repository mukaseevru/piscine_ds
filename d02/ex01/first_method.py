class Research:
    def file_reader(self):
        with open('data.csv', 'r') as input_file:
            return input_file.read()


if __name__ == '__main__':
    print(Research().file_reader())
