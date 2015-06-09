import sys
from concurrent.futures import ThreadPoolExecutor

from vlermv import cache
import requests

from . import parse

@cache('~/.gkebd', cache_exceptions = True)
def get(url, *args, **kwargs):
    return requests.get(url, *args, headers = { 'user-agent': 'https://pypi.python.org/pypi/gkebd'})

def startsidor():
    url = 'https://sv.wikipedia.org/wiki/Lista_%C3%B6ver_Sveriges_kommuner'
    with ThreadPoolExecutor(20) as e:
        for startsida, response in e.map(hitta_startsida, parse.kommuner(get(url))):
            if startsida, response != None:
                yield startsida, response

def hitta_startsida(kommun):
    for url in parse.hemsida(kommun):
        try:
            r = get(url, timeout = 10)
        except requests.exceptions.ConnectionError:
            pass
        except requests.exceptions.ReadTimeout:
            pass
        else:
            return kommun, url
    else:
         sys.stderr.write('Could not find a page for %s\n' % kommun)

def cli():
    import subprocess, json, tempfile
    import dataset

    fn = 'gkebd.sqlite'
    if os.path.exists(fn):
        os.remove(fn)
    db = dataset.connect('sqlite:///' + fn)

    tabell = {
        'startsida': db.get_table('startsidor', primary_id = 'kommun'),
        'skript': db.get_table('skript'),
        'kaka': db.get_table('kaka', primary_id = ('kommun', 'name')),
    }

    for kommun, startsida in startsidor():
        db['startsida'].insert({'kommun': kommun, 'startsida': startsida})

        for thirdparty in parse.tracking(get(startsida)):
            db['skript'].insert({'kommun': kommun, 'thirdparty': thirdparty})

        with tempfile.NamedTemporaryFile() as tmp:
            subprocess.call(['check-cookies.js', tmp.name, startsida])
            tmp.file.seek(0)
            for kaka in json.load(tmp.file):
                kaka['kommun'] = kommun
                db['kaka'].insert(kaka)
