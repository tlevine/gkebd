import re
from urllib.parse import urlparse

from lxml.html import fromstring
from unidecode import unidecode

def hemsida(kommun):
    '''
    >>> hemsida('Vetlanda kommun')
    'http://vetlanda.se'
    '''
    m = re.match(r'^(.+[^s])(s?) kommun$', kommun)
    if not m:
        assert False, kommun
    w = unidecode(m.group(1).lower())
    x = re.sub(r'[ -]', '', w)
    for scheme in ['http', 'https']:
        for prefix in ['', 'www.']:
            yield '%s://%s%s.se' % (scheme, prefix, x)
            if m.group(2) == 's':
                yield '%s://%s%ss.se' % (scheme, prefix, x)

def kommuner(response):
    html = fromstring(response.content)
    return filter(lambda text: text.endswith(' kommun'), html.xpath('//a/text()'))

def tracking(response):
    html = fromstring(response.content)
    html.make_links_absolute(response.url)

    o = urlparse(response.url)
    first_party = (o.scheme, o.netloc)

    for src in html.xpath('//script/@src'):
        p = urlparse(src)
        third_party = (p.scheme, p.netloc)
        if third_party != first_party:
            yield '%s://%s' % third_party
