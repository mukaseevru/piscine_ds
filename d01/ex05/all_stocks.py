import sys


def info(word):
    COMPANIES = {
        'Apple': 'AAPL',
        'Microsoft': 'MSFT',
        'Netflix': 'NFLX',
        'Tesla': 'TSLA',
        'Nokia': 'NOK'
    }
    STOCKS = {
        'AAPL': 287.73,
        'MSFT': 173.79,
        'NFLX': 416.90,
        'TSLA': 724.88,
        'NOK': 3.37
    }
    tickers = {v: k for k, v in COMPANIES.items()}
    ticker = word.upper()
    company = word.capitalize()
    if ticker in tickers:
        print(ticker, 'is a ticker symbol for', tickers[ticker])
    elif company in COMPANIES:
        print(company, 'stock price is', STOCKS[COMPANIES[company]])
    else:
        print(word, 'is an unknown company or an unknown ticker symbol')


def all_stocks(line):
    while ' ' in line:
        line = line.replace(' ', '')
    words = line.split(',')
    if '' in words:
        return
    for word in words:
        info(word)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        all_stocks(sys.argv[1])
