from vlermv import cache

from . import parse
from .check import check

get = cache('~/.gkebd')(requests.get)

def gkebd():
    url = 'https://sv.wikipedia.org/wiki/Lista_%C3%B6ver_Sveriges_kommuner'
    for kommun in parse.kommuner(get(url)):
        yield parse.tracking(get(parse.hemsida(kommun)))

def cli():
    import csv, sys
    for row in main():
        print(row)
