import json


class ReversoRequestMock:

    def __init__(self, text):
        self.text = text
        self.status_code = 200
        self.reason = 'test'


def get_reverso_browser_headers():
    with open('request_data/reverso_browser_headers.json', 'r') as reverso_browser_headers_file:
        return json.load(reverso_browser_headers_file)


def get_reverso_browser_cookies():
    with open('request_data/reverso_browser_cookies.json', 'r') as reverso_browser_cookies_file:
        return json.load(reverso_browser_cookies_file)


def get_reverso_request_mock():
    with open('request_data/reverso_request_mock.txt', 'r') as reverso_request_mock_file:
        content = reverso_request_mock_file.read()
    return ReversoRequestMock(content)
