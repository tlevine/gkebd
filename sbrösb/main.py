from vlermv import cache

from . import parse
from .check import check

get = cache('~/.sbrösb')(requests.get)

def main():
    url = 'https://sv.wikipedia.org/wiki/Lista_%C3%B6ver_Sveriges_kommuner'
    for kommun in parse.kommuner(get(url)):
        yield check(get(parse.hemsida(kommun)))

def cli():
    import csv, sys
    for row in main():
        print(row)
