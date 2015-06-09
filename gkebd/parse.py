import re
from urllib.parse import urlparse

from lxml.html import fromstring
from unidecode import unidecode

MANUAL = {
    'Dals-Eds kommun': 'http://www.dalsed.se',
    'Falu kommun': 'http://www.falun.se',
    'Hällefors kommun': None,
}
def gissa_startsida(kommun):
    if kommun in MANUAL:
        if MANUAL[kommun]:
            yield MANUAL[kommun]
    else:
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

    return html.xpath('//script/@src')

def startsida(url):
    p = urlparse(url)
    return '%s://%s' % (p.scheme, p.netloc)
