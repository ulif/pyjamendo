# List radio streams from jamendo.com.
#
# Requires Python 3.x.
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
try:                    # python 3.x
    from urllib.parse import urlencode
    from urllib.request import urlopen
except ImportError:     # python 2.x
    from urllib import urlencode
    from urllib import urlopen

BASE_URL = 'https://api.jamendo.com/v3.0'
CLIENT_ID = '56d30c95'  # for testing only

logger = logging.getLogger('pyjamendo')
logger.addHandler(logging.NullHandler())


def call_api(path, params):
    params.update(dict(client_id=CLIENT_ID, format='jsonpretty'))
    params = urlencode(params)
    url = '%s/%s?%s' % (BASE_URL, path, params)
    logger.info('Calling %s' % url)
    resp = urlopen(url)
    return json.loads(resp.read().decode('utf-8'))


## Uncomment for debugging
# logging.basicConfig(level=logging.DEBUG)
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
        stream_url = stream_descr['stream'].replace('https:', 'http:')
        print("#EXTINF:-1, Jamendo - %s\n%s" % (
            stream_descr['dispname'], stream_url))
