#!/usr/bin/python3
import timeit
import sys


def ft_lc():
    emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 'anna@live.com', 'philipp@gmail.com'] * 5
    return [x for x in emails if x.endswith('@gmail.com')]


def ft_loop():
    emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 'anna@live.com', 'philipp@gmail.com'] * 5
    lst = []
    for email in emails:
        if email.endswith('@gmail.com'):
            lst.append(email)
    return lst


def ft_map():
    emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 'anna@live.com', 'philipp@gmail.com'] * 5
    # return map(lambda x: x if x.endswith('@gmail.com') else None, emails)
    return list(map(lambda x: x if x.endswith('@gmail.com') else None, emails))


def ft_filter():
    emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 'anna@live.com', 'philipp@gmail.com'] * 5
    return list(filter(lambda x: x.endswith('@gmail.com'), emails))


def main():
    dct = {'loop': 'ft_loop',
           'list_comprehension': 'ft_lc',
           'map': 'ft_map',
           'filter': 'ft_filter'}
    if len(sys.argv) == 3:
        try:
            if sys.argv[1] in dct:
                print(timeit.timeit(dct[sys.argv[1]] + '()',
                                    number=int(sys.argv[2]),
                                    setup='from __main__ import ' + dct[sys.argv[1]]))
            else:
                print('Error in function')
        except ValueError:
            print('Error with number. Try ./benchmark.py loop 1000')


if __name__ == '__main__':
    main()
