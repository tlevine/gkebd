import re

from lxml.html import fromstring
from unidecode import unidecode

def hemsida(kommun):
    '''
    >>> hemsida('Vetlanda kommun')
    'http://vetlanda.se'
    '''
    m = re.match(r'(.*)s? kommun$', kommun)
    if not m:
        assert False, kommun
    return 'http://%s.se' % unidecode(m.group(1).lower())

def kommuner(response):
    html = fromstring(response)
    return filter(lambda href: href.endswith(' kommun'), html.xpath('//a/@href'))
