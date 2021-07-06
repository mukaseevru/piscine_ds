#!/usr/bin/python3
import timeit
import sys
from functools import reduce


def ft_loop(number):
    squares = 0
    for elem in range(1, int(number) + 1):
        squares += elem**2
    return squares


def ft_reduce(number):
    lst = [x for x in range(1, int(number) + 1)]
    return reduce(lambda x, y: x + y**2, lst)


def main():
    dct = {'loop': 'ft_loop',
           'reduce': 'ft_reduce'}
    if len(sys.argv) == 4:
        try:
            if sys.argv[1] in dct:
                print(timeit.timeit(dct[sys.argv[1]] + f'({int(sys.argv[3])})',
                                    number=int(sys.argv[2]),
                                    setup='from __main__ import ' + dct[sys.argv[1]]))
            else:
                print('Error in function')
        except ValueError:
            print('Error with number. Try ./benchmark.py loop 1000 5')


if __name__ == '__main__':
    main()
