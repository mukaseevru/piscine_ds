import sys


def names_extractor(path_to_file):
    with open(path_to_file, 'r') as input_file:
        with open('employees.tsv', 'w') as output_file:
            output_file.write('Name\tSurname\tE-mail\n')
            for line in input_file.readlines():
                name, surname = line.split('@')[0].split('.')
                name = name.capitalize()
                surname = surname.capitalize()
                output_file.write(f'{name}\t{surname}\t{line.strip()}\n')


if __name__ == '__main__':
    if len(sys.argv) == 2:
        names_extractor(sys.argv[1])
