import re
from http.client import responses
from typing import Dict

import httpx
from httpx import TimeoutException, InvalidURL, NetworkError
from pydantic import BaseModel


class ErrorReasons(BaseModel):
    reason: str
    url: str


class ResponseError(BaseModel):
    error: ErrorReasons


class StatusResponse(BaseModel):
    code: str
    phrase: str


class Response(BaseModel):
    id: int
    hop: int
    url: str
    http_version: str
    status_code: StatusResponse
    headers: Dict


class RedirectChecker:
    """
    Given a URL, trace the route taken and return the final destination.
    """

    def __init__(self, url):
        self.url = url
        self.resp = None
        self._json = {}
        self.response_information = []
        self.run()

    def run(self):
        try:
            self._resp()
            self.path_taken()
            return self.response_information
        except AttributeError as e:
            # TODO log e
            self._error("Invalid URL, or No Response Received.")
        except NetworkError as e:
            # TODO log e
            self._error(reason="The URL could not be resolved.")

    def _resp(self):

        with httpx.Client() as client:
            try:
                resp = client.get(self._http(), allow_redirects=True)
                self.resp = resp
            except TimeoutException as e:
                # TODO log e
                self._error("URL Response Timed Out.")
            except InvalidURL as e:
                # TODO log e
                self._error("Invalid URL, or No Response Received.")

    def _http(self):
        """
        Prepend the URL with 'http://' if not added manually by the user.
        :return: http:// + url
        """
        if not re.match("(?:http|https)://", self.url):
            return f"http://{self.url}"
        return self.url

    def _error(self, reason: str, url: str = None):
        """
        Error handling that bundles errors into pydantic classes and returns
        response_information as a json like response.
        """
        if url is None:
            url = self.url
        else:
            url = url

        error = ResponseError(error=ErrorReasons(reason=reason, url=url))
        self.response_information.append(error)

    def path_taken(self):
        hop = 0
        if self.resp.history:
            for url in self.resp.history:
                hop += 1
                response_data = Response(
                    id=hop,
                    hop=hop,
                    url=str(url.url),
                    http_version=url.http_version,
                    status_code=StatusResponse(
                        code=url.status_code, phrase=responses[int(url.status_code)]
                    ),
                    headers=dict(url.headers),
                )

                self.response_information.append(response_data)
            hop += 1
            response_data = Response(
                id=hop,
                hop=hop,
                url=str(self.resp.url),
                http_version=self.resp.http_version,
                status_code=StatusResponse(
                    code=self.resp.status_code,
                    phrase=responses[int(self.resp.status_code)],
                ),
                headers=dict(self.resp.headers),
            )

            self.response_information.append(response_data)
        else:
            hop = 1
            response_data = Response(
                id=hop,
                hop=hop,
                url=str(self.resp.url),
                http_version=self.resp.http_version,
                status_code=StatusResponse(
                    code=self.resp.status_code,
                    phrase=responses[int(self.resp.status_code)],
                ),
                headers=dict(self.resp.headers),
            )

            self.response_information.append(response_data)


# r = RedirectChecker("hi")
r = RedirectChecker("http://httpbin.org/")
# r = RedirectChecker("https://httpbin.org/redirect/2")
# print(r.response_information.error)
for resp in r.response_information:
    print(resp)
# print(r.response_information.error)
