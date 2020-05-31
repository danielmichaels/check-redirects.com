import logging
import re
import socket
from http.client import responses
from typing import Dict

import httpx
from httpx import TimeoutException, InvalidURL, NetworkError
from pydantic import BaseModel

from lib.util_logger import get_logger

logger = get_logger(__name__)


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
    host: str
    path: str
    scheme: str
    ipaddr: str
    time_elapsed: int


class RedirectChecker:
    """
    Given a URL, trace the route taken and return the final destination.
    """

    def __init__(self, url):
        self.url = url
        self.resp = None
        self.hop = 0
        self._json = {}
        self.response_information = []
        self.run()

    def run(self):
        try:
            self._resp()
            self.path_taken()
            return self.response_information
        except AttributeError as e:
            logging.error(e)
            self._error(reason="Invalid URL, or No Response Received.")
        except NetworkError as e:
            logger.error(e)
            self._error(reason="The URL could not be resolved.")

    def _resp(self):

        with httpx.Client() as client:
            try:
                resp = client.get(self._http(), allow_redirects=True)
                self.resp = resp
            except TimeoutException as e:
                logger.error(e)
                self._error("URL Response Timed Out.")
            except InvalidURL as e:
                logger.error(e)
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

    @staticmethod
    def _time_converter(resp):
        """
        Parses request.elapsed into milliseconds
        :param resp: response object
        :returns: integer that represents milliseconds
        """
        return int(resp.elapsed.total_seconds() * 1000)
        # return int(resp.elapsed * 1000)

    @staticmethod
    def _total_time_elapsed(resp):
        """
        Return the total time taken for all redirects.
        :param resp: response object
        :returns: sum of all response times in milliseconds.
        """
        total = []
        for redirects in resp.history:
            tt = redirects.elapsed.total_seconds()
            total.append(tt)
        total.append(resp.elapsed.total_seconds())
        return int(sum(total) * 1000)

    @staticmethod
    def _ipaddr(url):
        try:
            return socket.gethostbyname(url)
        except Exception as e:
            # log this
            logger.error(e)
            return "IP Could not be Resolved"

    def _response_info_loader(self, resp_type=None):
        self.hop += 1
        if resp_type is None:
            resp_type = self.resp
        else:
            resp_type = resp_type

        print(self._time_converter(resp_type))
        resp_obj = Response(
            id=self.hop,
            hop=self.hop,
            url=str(resp_type.url),
            http_version=resp_type.http_version,
            status_code=StatusResponse(
                code=resp_type.status_code,
                phrase=responses[int(resp_type.status_code)]
            ),
            host=resp_type.url.authority,
            scheme=resp_type.url.scheme,
            path=resp_type.url.path,
            ipaddr=self._ipaddr(resp_type.url.authority),
            time_elapsed=self._time_converter(resp_type),
            headers=dict(resp_type.headers),
        )
        self.response_information.append(resp_obj)

    def path_taken(self):
        if self.resp.history:
            for url in self.resp.history:
                self._response_info_loader(url)
            self._response_info_loader(self.resp)
        else:
            self._response_info_loader(self.resp)


r = RedirectChecker("hi")  # ERROR
# r = RedirectChecker("http://httpbin.org/") # DIRECT
# r = RedirectChecker("https://httpbin.org/redirect/2")  # REDIRECTS
# print(r.response_information.error)
for resp in r.response_information:
    print(resp)
# print(r.response_information.error)
