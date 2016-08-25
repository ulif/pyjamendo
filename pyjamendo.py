# List radio streams from jamendo.com.
#
# Jamendo distributes free music. It is free for private use.
#
# It also provides a couple of radio stations.
#
# This script uses jamendo API to determine the radio URLs and prints
# them in a form suitable for m3u files.
#
# The URLs are turned from https to http, because `cmus` cannot
# connect to https sources.
#
# See https://developer.jamendo.com/v3.0/read-methods for docs
#
import json
import logging
try:
    from urllib.parse import urlencode     # python 3.x
    from urllib.request import urlopen
except ImportError:                        # pragma: no cover
    from urllib import urlencode, urlopen  # python 2.x

__version__ = "0.1.1.dev0"

BASE_URL = 'https://api.jamendo.com/v3.0'
CLIENT_ID = '56d30c95'  # for testing only

logger = logging.getLogger('pyjamendo')
logger.addHandler(logging.NullHandler())
## Uncomment for debugging
# logging.basicConfig(level=logging.DEBUG)


def call_api(path, params):
    """Call the Jamendo API with `params`.

    `params` are parameters in a `dict()`.
    """
    params.update(dict(client_id=CLIENT_ID, format='jsonpretty'))
    params = urlencode(params)
    url = '%s/%s?%s' % (BASE_URL, path, params)
    logger.info('Calling %s' % url)
    resp = urlopen(url)
    return json.loads(resp.read().decode('utf-8'))


def jam_radios_to_m3u(allow_https_links=True):
    """Prints an EXTM3U-formatted list of jamendo radio stations.

    Jamendo web API is used to ask and list the stations in a format
    suitable for players like `winamp`, `cmus`, etc.

    Requires online connection.
    """
    result = call_api('radios/', dict())
    radios = result['results']
    print("#EXTM3U")
    for station in radios:
        logger.info('Handling station: %s' % station)
        details = call_api(
            'radios/stream/', dict(name=station['name']))
        logger.info('Station Details: %s' % details)
        details = details['results']
        for stream_descr in details:
            stream_url = stream_descr['stream']
            if not allow_https_links:
                stream_url = stream_url.replace('https:', 'http:')
            print("#EXTINF:-1, Jamendo - %s\n%s" % (
                stream_descr['dispname'], stream_url))


if __name__ == "__main__":  # pragma: no cover
    jam_radios_to_m3u(allow_https_link=False)
