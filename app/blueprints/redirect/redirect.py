import httpx
from httpx._exceptions import TimeoutException
from httpx import URL, Response
from urllib3.util import Url


class RedirectChecker:
    """
    Given a URL, trace the route taken and return the final destination.
    """

    def __init__(self, url):
        self.url = url
        self.resp = None

    def _resp(self):

        with httpx.Client() as client:
            try:
                resp = client.get(self.url)
                self.resp = resp
            except TimeoutException() as e:
                print(e)

    def path_taken(self):
        if self.resp.history:
            hop = 0
            for url in self.resp.history:
                hop += 1
                print(f'{hop} URL: {url.url}')


r = RedirectChecker('http://httpbin.org/redirect/2')
r._resp()
r.path_taken()
