import sys


def caesar(string, shift):
    try:
        string.encode('ascii')
    except UnicodeEncodeError:
        raise Exception('The script does not support your language yet')

    lowerletters = list('abcdefghijklmnopqrstuvwxyz')
    upperletters = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    new_string = ''
    for letter in string:
        if letter in lowerletters:
            new_string += lowerletters[(lowerletters.index(letter) + shift) % 26]
        elif letter in upperletters:
            new_string += upperletters[(upperletters.index(letter) + shift) % 26]
        else:
            new_string += letter
    return new_string


if __name__ == '__main__':
    if len(sys.argv) == 4:
        if sys.argv[1] == 'encode':
            print(caesar(sys.argv[2], int(sys.argv[3])))
        elif sys.argv[1] == 'decode':
            print(caesar(sys.argv[2], -int(sys.argv[3])))
        else:
            raise Exception('Error. Try python3 caesar.py encode \'ssh -i private.key user@school21.ru\' 12')
    else:
        raise Exception('Error. Try python3 caesar.py encode \'ssh -i private.key user@school21.ru\' 12')
