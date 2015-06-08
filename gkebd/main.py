import sys

from vlermv import cache
import requests

from . import parse

get = cache('~/.gkebd', cache_exceptions = True)(requests.get)

def gkebd():
    url = 'https://sv.wikipedia.org/wiki/Lista_%C3%B6ver_Sveriges_kommuner'
    for kommun in parse.kommuner(get(url)):
        for url in parse.hemsida(kommun):
            try:
                r = get(url, timeout = 10)
            except requests.exceptions.ConnectionError:
                pass
            else:
                yield kommun, parse.tracking(r)
                break
        else:
             sys.stderr.write('Could not find a page for %s\n' % kommun)

def cli():
    import csv
    w = csv.writer(sys.stdout)
    w.writerow(('kommun', 'third.party'))
    for kommun, trackers in gkebd():
        for tracker in trackers:
            w.writerow((kommun, tracker))
