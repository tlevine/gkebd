import sys
from concurrent.futures import ThreadPoolExecutor

from vlermv import cache
import requests

from . import parse

@cache('~/.gkebd', cache_exceptions = True)
def get(url, *args, **kwargs):
    return requests.get(url, *args, headers = { 'user-agent': 'https://pypi.python.org/pypi/gkebd'})

def gkebd():
    url = 'https://sv.wikipedia.org/wiki/Lista_%C3%B6ver_Sveriges_kommuner'
    with ThreadPoolExecutor(20) as e:
        for row in e.map(gkebd_one, parse.kommuner(get(url))):
            if row != None:
                yield row

def gkebd_one(kommun):
    for url in parse.hemsida(kommun):
        try:
            r = get(url, timeout = 10)
        except requests.exceptions.ConnectionError:
            pass
        except requests.exceptions.ReadTimeout:
            pass
        else:
            return kommun, parse.tracking(r)
    else:
         sys.stderr.write('Could not find a page for %s\n' % kommun)

def cli():
    import csv
    w = csv.writer(sys.stdout)
    w.writerow(('kommun', 'third.party'))
    for kommun, trackers in gkebd():
        for tracker in trackers:
            w.writerow((kommun, tracker))
