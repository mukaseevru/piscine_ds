def read_and_write():
    # with open('d01_ds.csv', 'r') as csv_file:
    with open('ds.csv', 'r') as csv_file:
        with open('ds.tsv', 'w') as tsv_file:
            text = csv_file.read()\
                .replace('\",', '\"\t')\
                .replace('false,', 'false\t')\
                .replace('true,', 'true\t')
            tsv_file.write(text)


if __name__ == '__main__':
    read_and_write()
