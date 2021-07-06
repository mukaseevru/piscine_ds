#!lnickole/bin/python3
import os


def main():
    print(f"Your current virtual env is {os.environ['VIRTUAL_ENV']}")


if __name__ == '__main__':
    main()
