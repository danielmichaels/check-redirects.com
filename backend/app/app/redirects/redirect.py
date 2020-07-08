"""
Redirect core functionality.
"""
import logging
import re
import socket
from http.client import responses

import httpx
from app.schemas.redirect import ResponseError, ErrorReasons, Response, \
    StatusResponse
from httpx import InvalidURL, NetworkError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
        """
        entrypoint for redirect class.
        """
        try:
            self._resp()
            self.path_taken()
            return self.response_information
        except AttributeError as err:
            logging.error(err)
            self._error(reason="Invalid URL, or No Response Received.")
        except NetworkError as err:
            # generic error that captures URL's which do not exist
            # set logger.error() to enable sentry to track this.
            logger.info(err)
            self._error(reason="The URL could not be resolved.")

    def _resp(self):

        with httpx.Client() as client:
            try:
                resp = client.get(self._http(), allow_redirects=True)
                self.resp = resp
            except InvalidURL as err:
                logger.error(err)
                self._error(reason="Invalid URL, or No Response Received.")

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

    @staticmethod
    def _total_time_elapsed(resp):
        """
        Return the total time taken for all redirects.
        :param resp: response object
        :returns: sum of all response times in milliseconds.
        """
        total = []
        for redirects in resp.history:
            time_taken = redirects.elapsed.total_seconds()
            total.append(time_taken)
        total.append(resp.elapsed.total_seconds())
        return int(sum(total) * 1000)

    @staticmethod
    def _ipaddr(url):
        try:
            return socket.gethostbyname(url)
        except Exception as err:
            logger.error(err)
            return "IP Could not be Resolved"

    def _response_info_loader(self, resp_type=None):
        """
        Loader class which places response information into relevant
        pydantic containers.
        """
        self.hop += 1
        if resp_type is None:
            resp_type = self.resp

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
        """
        HTTPX returns the final response and a history dictionary. To extract
        the hops before the final destination, the history objects must be looped
        over in order to obtain each hop's data. Any data extracted is loaded
        into a Response pydantic container.
        """
        if self.resp.history:
            for url in self.resp.history:
                self._response_info_loader(url)
            self._response_info_loader(self.resp)
        else:
            self._response_info_loader(self.resp)

# r = RedirectChecker("hi")  # ERROR
# r = RedirectChecker("http://httpbin.org/") # DIRECT
# r = RedirectChecker("https://httpbin.org/redirect/2")  # REDIRECTS
# print(r.response_information)
# for resp in r.response_information:
#     print(resp)
# print(r.response_information.error)
