#!lnickole/bin/python3
import sys
import time
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request


def financial(ticker, row):
    url = 'https://finance.yahoo.com/quote/' + ticker + '/financials'
    page = urlopen(Request(url=url)).read()
    page_parsed = BeautifulSoup(page, 'html.parser')
    title = page_parsed.title.string
    if title == 'Symbol Lookup from Yahoo Finance':
        raise Exception('Wrong ticker')
    tags = page_parsed.find_all(attrs={'data-test': 'fin-row'})
    rows = [tag.find(class_='Va(m)').get_text() for tag in tags]
    if row not in rows:
        raise Exception('Error with row')
    elems = tags[rows.index(row)].find_all('span')
    time.sleep(5)
    return tuple(elem.get_text() for elem in elems)


if __name__ == '__main__':
    if len(sys.argv) == 3:
        print(financial(sys.argv[1], sys.argv[2]))
