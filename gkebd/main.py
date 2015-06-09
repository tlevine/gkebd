import os, sys
import subprocess, json, tempfile
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor, as_completed

from vlermv import cache
import requests

from . import parse

@cache('~/.gkebd', cache_exceptions = True)
def get(url, *args, **kwargs):
    return requests.get(url, *args, allow_redirects = False,
        headers = {'user-agent': 'https://pypi.python.org/pypi/gkebd'})

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
        futures = {e.submit(hitta_startsida, k): url for k in parse.kommuner(get(url))}
        for future in as_completed(futures):
            if future.exception():
                sys.stderr.write('Exception at %s' % futures[future])
            else:
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
  value TEXT,
  domain TEXT,
  path TEXT,
  httponly INTEGER,
  secure INTEGER,
  expires TEXT,
  expiry TEXT,

  UNIQUE(kommun, name)
)''')

    with ThreadPoolExecutor(8) as e:
        for kommun, startsida in startsidor():
            e.submit(gkebd, db, kommun, startsida)

    sql = '''select kommun || ' (' || startsida || ')' as "x" from startsida where kommun not in (select kommun from kaka union select kommun from skript);'''
    msg = 'Kommuner som använder varken skript eller kakor:\n%s\n'
    sys.stdout.write(msg % '\n'.join(row['x'] for row in db.engine.execute(sql)))

#   for kommun, startsida in startsidor():
#       gkebd(db, kommun, startsida)

def gkebd(db, kommun, startsida):
    db['startsida'].insert({'kommun': kommun, 'startsida': startsida})

    for thirdparty in parse.tracking(get(startsida)):
        db['skript'].insert({'kommun': kommun, 'thirdparty': thirdparty})

    kakor = check_cookies(startsida)
    for kaka in kakor:
        kaka['kommun'] = kommun
    db['kaka'].insert_many(kakor)
