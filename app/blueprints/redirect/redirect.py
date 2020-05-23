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
                resp = client.get(self.url, allow_redirects=True)
                self.resp = resp
            except TimeoutException() as e:
                print(e)

    def path_taken(self):
        hop = 0
        if self.resp.history:
            for url in self.resp.history:
                hop += 1
                # print(
                #     f"[{url.status_code}] {hop} URL: {url.url} - headers: {type(url.headers)}"
                # )
                self._json["hop"] = hop
                self._json["url"] = str(url.url)
                self._json["statusCode"] = [
                    {
                        "code": url.status_code,
                        "phrase": responses[int(url.status_code)],
                    }
                ]
                self._json["headers"] = dict(url.headers) #TODO: consider creating custom serializer for this
                self.json_list.append(self._json.copy())
        # print(f"[{self.resp.status_code}] {hop + 1} URL: {self.resp.url}")
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


# r = RedirectChecker("http://httpbin.org/redirect/5")
# print(r.json_list)
