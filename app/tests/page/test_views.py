from flask import url_for

from lib.tests import ViewTestMixin, assert_status_with_message


class TestPage(ViewTestMixin):
    def test_home_page(self):
        """ Home page should respond with a success 200. """
        response = self.client.get(url_for("page.home"))
        assert response.status_code == 200
        assert b"Check Redirects" in response.data

    def test_home_page_search_url_not_exist(self):
        """ Home page search for URL that does not exist. """
        form = {"search": "http://doesnotexist123fourfivesixe.com"}

        response = self.client.post(
            url_for("page.home"), data=form, follow_redirects=True
        )
        assert response.status_code == 200
        assert b"Error" in response.data

    def test_home_page_search_url_does_exist(self):
        """ Home page search for URL that does exist. """
        form = {"search": "http://httpbin.org"}

        response = self.client.post(
            url_for("page.home"), data=form, follow_redirects=True
        )
        assert response.status_code == 200
        assert b"Final Redirect" in response.data

    def test_terms_page(self):
        """ Terms page should respond with a success 200. """
        response = self.client.get(url_for("page.terms"))
        assert response.status_code == 200

    def test_privacy_page(self):
        """ Privacy page should respond with a success 200. """
        response = self.client.get(url_for("page.privacy"))
        assert response.status_code == 200

    def test_404_page(self):
        """ 404 errors should show the custom 404 page. """
        response = self.client.get("/nochancethispagewilleverexistintheapp")

        assert_status_with_message(404, response, "Error 404")
