import requests
from requests import HTTPError
from bs4 import BeautifulSoup

from request_helper import get_reverso_browser_headers, get_reverso_browser_cookies, get_reverso_request_mock

MAIN_TRANSLATION_URL = 'https://context.reverso.net/translation'


def get_translation_direction(source_lang: str) -> str:
    if 'eng' in source_lang.lower():
        return 'english-russian'

    if 'ru' in source_lang.lower():
        return 'russian-english'


def parse_response(text: str) -> list:
    translations = []
    page = BeautifulSoup(text, "html.parser")
    translations_content = page.findChild('div', {'id': 'translations-content'})

    for translations_item in translations_content.find_all('a', {'class', 'translation'}):
        translations.append(translations_item.text.strip('\n'))

    return translations


def get_translation(word: str, source_lang: str = 'eng') -> str:
    translation_direction = get_translation_direction(source_lang)
    translation_url = f'{MAIN_TRANSLATION_URL}/{translation_direction}/{word}'

    # response = requests.get(
    #     translation_url,
    #     cookies=get_reverso_browser_cookies(),
    #     headers=get_reverso_browser_headers(),
    # )
    response = get_reverso_request_mock()
    if response.status_code > 300:
        raise HTTPError(response.reason)

    if response.text:
        parse_response(response.text)
        return response.text

    return ''


get_translation('prompt')
