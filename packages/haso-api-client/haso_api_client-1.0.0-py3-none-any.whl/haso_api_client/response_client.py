from . import exceptions


class Response:
    def __init__(self, response):
        self.status_code = response.status_code
        self.headers = response.headers
        self.content = response.content
        self.json_data = None

        try:
            self.json_data = response.json()
        except ValueError:
            pass

    def raise_for_status(self):
        if self.status_code >= 400:
            raise exceptions.HTTPError(f"HTTP error {self.status_code}", response=self)

    def __repr__(self):
        return f"<Response [{self.status_code}]>"
