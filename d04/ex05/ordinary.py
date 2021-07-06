#!/usr/bin/python3
import sys
import psutil


def ordinary(path):
    with open(path, 'r') as input_file:
        lst = input_file.readlines()
    return lst


def main():
    if len(sys.argv) == 2:
        for line in ordinary(sys.argv[1]):
            pass
        mem = psutil.Process().memory_info().vms / 2 ** 30
        cpu = psutil.Process().cpu_times()
        print(f'Peak Memory Usage = {mem:.3f} Gb')
        print(f'User Time + System Time = {cpu.user + cpu.system:.2f}s')


if __name__ == '__main__':
    main()
