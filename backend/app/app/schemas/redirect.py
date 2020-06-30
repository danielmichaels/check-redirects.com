from typing import Dict

from pydantic import BaseModel


class ErrorReasons(BaseModel):  # pylint: disable=too-few-public-methods
    """ Error pydantic container. """

    reason: str
    url: str


class ResponseError(BaseModel):  # pylint: disable=too-few-public-methods
    """ Error pydantic container. """

    error: ErrorReasons


class StatusResponse(BaseModel):  # pylint: disable=too-few-public-methods
    """ Status pydantic container. """

    code: str
    phrase: str


class Response(BaseModel):  # pylint: disable=too-few-public-methods
    """ Response pydantic container. """

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
