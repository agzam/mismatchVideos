import json
import eventlet
from eventlet.green import urllib

base_url = "https://stg-apiv2.vevo.com"


def get_api_token():
    data = {
        "client_id": "",
        "client_secret": "",
        "grant_type": "client_credentials",
        "country": "US",
        "locale": "en-us"
    }

    data = urllib.urlencode(data)
    url = "{base_url}/oauth/token".format(base_url=base_url)
    req = urllib.urlopen(url, data)
    ob = json.loads(req.read())
    return ob['access_token']


def get_data(url):
    f = urllib.urlopen(url)
    return f.read()


if __name__ == '__main__':
    api_token = get_api_token()
    pool = eventlet.GreenPool()
    url_str = "{base_url}/videos?page={page}&size=100&genre=&sort=MostViewedAllTime&token={token}"
    urls = {url_str.format(base_url=base_url, token=api_token, page=p) for p in range(1, 500)}

    for body in pool.imap(get_data, urls):
        if body:
            try:
                jsn = json.loads(body)
                if jsn.has_key('videos'):
                    for v in jsn['videos']:
                        if ('explicit' in v['title'].lower()) and (v['isExplicit'] == False):
                            print v['isrc'] + ' ' + v['title']
            except ValueError:
                continue

