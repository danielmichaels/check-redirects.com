""""""
from typing import List

from app import schemas
from app.redirects.redirect import RedirectChecker
from app.schemas.redirect import SearchForm
from fastapi import APIRouter

router = APIRouter()


@router.post("/checker", response_model=List[schemas.Response])
def check_redirect(form_data: SearchForm):
    """
    URL which will be checked for redirects.

    :param form_data: form data containing URL to search
    """
    form_data = form_data.dict()
    if form_data:
        redirects = RedirectChecker(form_data["url"])
        response = redirects.response_information
        return response
