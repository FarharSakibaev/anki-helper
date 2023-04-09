import time

import requests
from bs4 import BeautifulSoup


def get_wordlist() -> list:
    words = 'implement, invoke, hesitate, satire, realize, silly, occasion, restroom, cattle, prefer, genre, dangle, ' \
            'supplies, kite, until, deck, regret, flu, flea, missiles, retired,  abandoned, van, headquarters, ' \
            'endeavoring, riffed off, vitriolic rants, persist, lurid, hoax, grisly, tableaux, amplify, sow, ' \
            'efforts, disputing, propaganda, sleazy, innocent,  landmark,  ballots, fulfill, lettuce, efficient, ' \
            'appointment, prescription, stomach, pollution, toothache, tot, obviously, apparently, evidently, ' \
            'patently, rewind, Hesitate, predict, proceed, forecast, prediction, influence, Companion, interlocutor, ' \
            'collator, company, Hurry, Consider, Throw, Currency, Definitely, correctness, rightwards, rectitude, ' \
            'rightness'
    word_list = [item.lower() for item in words.split(', ')]
    return list(set(word_list))


def get_url() -> str:
    for word in get_wordlist():
        yield str(f'https://dictionary.cambridge.org/dictionary/english/{word}')


def get_page(url: str) -> BeautifulSoup:
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " \
                 "(KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36"

    headers = {'User-Agent': user_agent}
    try:
        web_request = requests.get(url, headers=headers)
        return BeautifulSoup(web_request.text, "html.parser")
    except Exception as ex:
        raise RuntimeError(f'An error occurred while processing url {url}: {str(ex)}')


def get_word(page: BeautifulSoup, url) -> str:
    word = page.findChild('span', {'class': 'dhw'})
    if word is None:
        raise RuntimeError('word is none on ' + url)

    return word.text.strip() + '\t'


def get_transcription(page: BeautifulSoup, url: str) -> str:
    transcription = page.findChild('span', {'class': 'dpron'})
    if transcription is None:
        raise RuntimeError('transcription is none on ' + url)

    return transcription.text.strip() + '<br>'


def get_word_string(url: str) -> str:
    page = get_page(url)
    word = get_word(page, url)

    word += get_transcription(page, url)

    type_of_word = page.findChild('span', {'class': 'dpos'}).text.strip()
    word += '<i>' + type_of_word + '</i><br>'

    meanings_block = page.find_all('div', {'class': 'ddef_block'})
    if meanings_block is None:
        print('meanings_block is none on ' + url)
        return ''

    for meaning in page.find_all('div', {'class': 'ddef_block'}):

        current_meaning = meaning.findChild('div', {'class': 'ddef_d'})
        if current_meaning is not None:

            type_of_word_to_meaning = meaning.findChild('div', {'class': 'dpos'})
            if type_of_word_to_meaning is not None and type_of_word != type_of_word_to_meaning:
                word += '<i>' + type_of_word_to_meaning.text.strip() + '</i><br>'

            word += current_meaning.text.strip() + '<br>'  # meaning
            for example in meaning.findChildren('div', {'class': 'dexamp'}):
                word += '- ' + example.text.strip() + '<br>'

            word += '<br>'

    return word


def write_to_txt(word_string_list) -> None:
    with open('words.txt', 'w') as output:
        output.write('\n'.join(word_string_list))


def run() -> None:
    result = []
    for url in get_url():
        try:
            word = get_word_string(url)
            result.append(word)
            time.sleep(1)
        except RuntimeError as ex:
            print(str(ex))
    write_to_txt(result)


if __name__ == '__main__':
    run()
