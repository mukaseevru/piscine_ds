def dict_sorter():
    list_of_tuples = [
        ('Russia', '25'),
        ('France', '132'),
        ('Germany', '132'),
        ('Spain', '178'),
        ('Italy', '162'),
        ('Portugal', '17'),
        ('Finland', '3'),
        ('Hungary', '2'),
        ('The Netherlands', '28'),
        ('The USA', '610'),
        ('The United Kingdom', '95'),
        ('China', '83'),
        ('Iran', '76'),
        ('Turkey', '65'),
        ('Belgium', '34'),
        ('Canada', '28'),
        ('Switzerland', '26'),
        ('Brazil', '25'),
        ('Austria', '14'),
        ('Israel', '12')
    ]
    dct = {}
    for elem in list_of_tuples:
        if int(elem[1]) in dct:
            dct[int(elem[1])].append(elem[0])
        else:
            dct[int(elem[1])] = [elem[0]]

    for number in sorted(dct, reverse=True):
        for country in sorted(dct[number]):
            print(country)


if __name__ == '__main__':
    dict_sorter()
