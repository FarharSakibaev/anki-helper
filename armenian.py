import re
import time

import requests
from bs4 import BeautifulSoup


def is_russian(text):
    return bool(re.search('[а-яА-Я]', text))


def get_wordlist() -> list:
    words = 'նա, դաս, մատ, մաս, մազ, իմ, մի, միս, իսկ, կին, դու, ում, ուս, մուկ, տուն, Եկ, ես, եզ, ' \
            'ետ, ելակ, մեկ, տես, տեսնել, մեկնել, կետ, կես, կիսել, լեզու, լիզել, անել, տանել, ուտել, ասել, ' \
            'էլ, էլի, դե		,զե	,եզ,դեզ,կե	,եկ,մեկ,լե	,ել,ուտել,մե		,դեմ,նե		,դեն,սե	,ես,կես,տե	,' \
            'ետ,կետ, մուկ, կատու, կետ, մատիտ,Ընկա, ընտանի, տուն, մուկ, կետ, մատ, մատիտ, Հայուհի, հայկական, Հայաստան, ' \
            'Հայկազ, Հայկազյան, հույզ, հազալ, հատիկ, Հուսիկ, Սահակ, Սահակյան, սահնակ, Հնդկաստան, հնդիկ, էհ, Ռուս, ' \
            'Ռուսաստան, ռազմիկ, Ռուզան, ամառ, լեռ, անտառ, նուռ, Հայր, հայրիկ, հայրենի, մայր, մայրիկ, մայրենի, մարմար, ' \
            'նարդի, դիր, տար, տուր, մուր, սուր, սար, Արարատ, Արա, հյուր, կույր, երես, ռուսերեն, հայերեն, լատիներեն, ' \
            'լեհերեն, Ամերիկա, Մատենադարան, համալսարան, կարմիր, ընտիր, ընկեր, կրակ, նրա, լրատու, դրամ, Ղեկ, տեղ, ' \
            'այստեղ, այդտեղ, այնտեղ, ամեն տեղ, սեղան, տաղ, եղանակ, դեղ, մեղու, սուղ, նեղ, աղեղ, ուղեղ, աղ, մաղ, ' \
            'մեղր, դղյակ, կղզի, տղա, Դաղստան, աստղ, Քանակ, քույր, հայրենիք, քեզ, քար, տաք, քսել, քնել, մենք, դուք, ' \
            'նրանք, մենք ասում ենք, դուք ասում եք, նրանք ասում են, մենք այստեղ ենք, դուք այդտեղ եք, նրանք այնտեղ են, այսինքն'
    word_list = [item.lower().strip() for item in words.split(',')]
    return list(set(word_list))[115:]


def get_url() -> str:
    word_list = get_wordlist()
    for word in word_list:
        if ' ' in word:
            print(word + ' has space')
            continue
        yield str(f'https://bararanonline.com/{word}')


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
    word = page.findChild('span', {'class': 'word_name'})
    if word is None:
        raise RuntimeError('word is none on ' + url)

    return word.text.strip() + '\t'


def get_transcription(page: BeautifulSoup, url: str) -> str:
    words = page.findChildren('div', {'class': 'content-core-arm'})
    for word in words:
        if word is None:
            raise RuntimeError('word is none on ' + url)

        if is_russian(word.text):
            return word.text.strip() + '\t'

    return ''


def get_word_string(url: str) -> str:
    page = get_page(url)
    word = get_word(page, url)

    if not word:
        return ''

    transcription = get_transcription(page, url)

    if not transcription:
        return ''

    word += get_transcription(page, url)

    return word


def write_to_txt(word_string_list) -> None:
    with open('words.txt', 'w') as output:
        output.write('\n'.join(word_string_list))


def run() -> None:
    result = []
    for url in get_url():
        try:
            word = get_word_string(url)
            if not word:
                continue
            result.append(word)
            time.sleep(5)
        except RuntimeError as ex:
            print(str(ex))
    write_to_txt(result)


if __name__ == '__main__':
    run()
