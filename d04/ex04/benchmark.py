#!/usr/bin/python3
import timeit
import random
from collections import Counter


def my_function(lst):
    dct = {}
    for elem in lst:
        if elem in dct:
            dct[elem] += 1
        else:
            dct[elem] = 1
    return dct


def my_top(lst):
    dct = my_function(lst)
    return sorted(dct.items(), key=(lambda x: -x[1]))[:10]


def main():
    lst = [random.randint(0, 100) for x in range(1000000)]
    print('my function:',
          timeit.timeit(f'my_function({lst})',
                        number=1,
                        setup='from __main__ import my_function'))
    print('Counter:',
          timeit.timeit(f'Counter({lst})',
                        number=1,
                        setup='from __main__ import Counter'))
    print('my top:',
          timeit.timeit(f'my_top({lst})',
                        number=1,
                        setup='from __main__ import my_top'))
    print('Counter\'s top:',
          timeit.timeit(f'Counter({lst}).most_common(10)',
                        number=1,
                        setup='from __main__ import Counter'))


if __name__ == '__main__':
    main()
