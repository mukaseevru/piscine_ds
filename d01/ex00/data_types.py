def data_types():
    a = 0
    b = ''
    c = 0.0
    d = True
    e = []
    f = {}
    g = ()
    i = set()
    print(
        f'[{type(a).__name__}, '
        f'{type(b).__name__}, '
        f'{type(c).__name__}, '
        f'{type(d).__name__}, '
        f'{type(e).__name__}, '
        f'{type(f).__name__}, '
        f'{type(g).__name__}, '
        f'{type(i).__name__}]'
    )


if __name__ == '__main__':
    data_types()
