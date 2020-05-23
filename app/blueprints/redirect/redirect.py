import re
from http.client import responses

import httpx
from httpx import TimeoutException, Headers, InvalidURL


class RedirectChecker:
    """
    Given a URL, trace the route taken and return the final destination.
    """

    def __init__(self, url):
        self.url = url
        self.resp = None
        self._json = {}
        self.json_list = []
        self.run()

    def run(self):
        try:
            self._resp()
            self.path_taken()
            return self.json_list
        except AttributeError as e:
            self.json_list.append({"error": "Invalid URL"})
            print(f"Attribute Error: {e}")

    def _resp(self):

        with httpx.Client() as client:
            try:
                resp = client.get(self._http(), allow_redirects=True, timeout=5.1)
                self.resp = resp
            except TimeoutException as e:
                self.json_list.append({"error": "URL Timed Out"})
            except InvalidURL as e:
                # log this though

    def _http(self):
        """
        Prepend the URL with 'http://' if not added manually by the user.
        :return: http:// + url
        """
        if not re.match("(?:http|https)://", self.url):
            return f"http://{self.url}"
        return self.url

    def path_taken(self):
        hop = 0
        if self.resp.history:
            for url in self.resp.history:
                hop += 1
                self._json["hop"] = hop
                self._json["url"] = str(url.url)
                self._json["statusCode"] = [
                    {
                        "code": url.status_code,
                        "phrase": responses[int(url.status_code)],
                    }
                ]
                self._json["headers"] = dict(
                    url.headers
                )
                self.json_list.append(self._json.copy())
        self._json["hop"] = hop + 1
        self._json["url"] = str(self.resp.url)
        self._json["statusCode"] = [
            {
                "code": self.resp.status_code,
                "phrase": responses[int(self.resp.status_code)],
            }
        ]
        self._json["headers"] = dict(self.resp.headers)
        self.json_list.append(self._json)


r = RedirectChecker("hi")
# r = RedirectChecker("http://httpbin.org/redirect/2")
# r = RedirectChecker("https://httpbin.org/redirect/2")
print(r.json_list)
