#!/usr/bin/python3
import timeit


def ft_lc():
    emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 'anna@live.com', 'philipp@gmail.com'] * 5
    return [email for email in emails if email.endswith('@gmail.com')]


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


def main():
    loop_time = timeit.timeit('ft_loop()',
                              setup='from __main__ import ft_loop',
                              number=90_000_000)
    lc_time = timeit.timeit('ft_lc()',
                            setup='from __main__ import ft_lc',
                            number=90_000_000)
    map_time = timeit.timeit('ft_map()',
                             setup='from __main__ import ft_map',
                             number=90_000_000)
    if (loop_time < lc_time) & (loop_time < map_time):
        print('it is better to use a loop')
    elif (lc_time <= loop_time) & (lc_time <= map_time):
        print('it is better to use a list comprehension')
    else:
        print('it is better to use a map')
    sorted_time = sorted([loop_time, lc_time, map_time])
    print(f'{sorted_time[0]} vs {sorted_time[1]} vs {sorted_time[2]}')


if __name__ == '__main__':
    main()
