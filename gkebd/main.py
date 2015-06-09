import os, sys
import subprocess, json, tempfile
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor, as_completed

from vlermv import cache
import requests

from . import parse

@cache('~/.gkebd', cache_exceptions = True)
def get(url, *args, **kwargs):
    return requests.get(url, *args, follow_redirects = False,
        headers = { 'user-agent': 'https://pypi.python.org/pypi/gkebd'})

@cache('~/.gkebd-cookies', serializer = json)
def check_cookies(url):
    with tempfile.NamedTemporaryFile(mode = 'r+') as tmp:
        subprocess.call(['check-cookies.js', tmp.name, url])
        tmp.file.seek(0)
        cookies = json.load(tmp.file)
    return cookies

def startsidor():
    url = 'https://sv.wikipedia.org/wiki/Lista_%C3%B6ver_Sveriges_kommuner'
    with ThreadPoolExecutor(20) as e:
        futures = (e.submit(hitta_startsida, k) for k in parse.kommuner(get(url)))
        for future in as_completed(futures):
            yield future.result()

def hitta_startsida(kommun):
    for url in parse.gissa_startsida(kommun):
        try:
            r = get(url, timeout = 10)
        except requests.exceptions.ConnectionError:
            pass
        except requests.exceptions.ReadTimeout:
            pass
        else:
            t = r.text.lower()
            if 'kommun' in t:
                return kommun, url
    else:
        sys.stderr.write('Could not find a page for %s\n' % kommun)
        return None, None

def cli():
    import dataset

    fn = '/tmp/gkebd.sqlite'
    if os.path.exists(fn):
        os.remove(fn)
    db = dataset.connect('sqlite:///' + fn)
    db.engine.execute('CREATE TABLE startsida (kommun TEXT, UNIQUE(kommun))')
    db.engine.execute('''
CREATE TABLE kaka (
  kommun TEXT NOT NULL,
  name TEXT NOT NULL,
  value TEXT NOT NULL,
  domain TEXT NOT NULL,
  path TEXT NOT NULL,
  httponly INTEGER NOT NULL,
  secure INTEGER NOT NULL,
  expires TEXT NOT NULL,
  expiry TEXT NOT NULL,

  UNIQUE(kommun, name)
)''')

#   with ThreadPoolExecutor(8) as e:
#       for kommun, startsida in startsidor():
#           e.submit(gkebd, db, kommun, startsida)
    for kommun, startsida in startsidor():
        gkebd(db, kommun, startsida)

def gkebd(db, kommun, startsida):
    db['startsida'].insert({'kommun': kommun, 'startsida': startsida})

    for thirdparty in parse.tracking(get(startsida)):
        db['skript'].insert({'kommun': kommun, 'thirdparty': thirdparty})

    kakor = check_cookies(startsida)
    for kaka in kakor:
        kaka['kommun'] = kommun
    db['kaka'].insert_many(kakor)
