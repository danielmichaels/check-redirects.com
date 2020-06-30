""""""
from app.redirects.redirect import RedirectChecker
from fastapi import APIRouter, Form

router = APIRouter()


@router.post("/check-it")
def check_redirect(url: str = Form(...)):
    """
    URL which will be checked for redirects.

    :param url: url to be checked
    """
    redirects = RedirectChecker(url)
    response = redirects.response_information

    return {"response": response}
