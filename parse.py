import urllib
import re
import pickle
from bs4 import BeautifulSoup


def get_whole_text(url):
    file = urllib.request.urlopen(url)
    html = file.read()
    soup = BeautifulSoup(html, features="html5lib")

    for script in soup(['script', 'style']):
        script.extract()

    text = soup.get_text()
    return text


def find_dates(text):
    start1 = 'А. П. ЧЕХОВ И АЛ. П. ЧЕХОВ'
    start2 = 'А. П. ЧЕХОВ В ПЕРЕПИСКЕ С СОВРЕМЕННИКАМИ'
    letters_info = [string.strip() for string in text[text.find(start1): text.find(start2)].split('\n')]
    letters_info = [string for string in letters_info if string != '' and not string.startswith('А. П. ЧЕХОВ ')]

    pattern = r'(Чехов -- [\. а-яА-ЯёЁ]*\. )|([\. а-яА-ЯёЁ]* -- Чехову. )'
    dates_info = dict()
    for letter_info in letters_info:
        match = re.search(pattern, letter_info)
        if match:
            dates_info[letter_info] = letter_info[len(match[0]):]

    cutted_text = text[text.find(start2):]

    dates_info['Чехов -- A. Н. Плещееву. 19 января 1888 г. Москва'] = '19 января 1888 г. Москва'
    dates_info['Чехов -- Н. А. Лейкину. 22 марта 1885 г. Москва'] = '22 марта 1885 г. Моста'
    dates_info['Чехов -- Н. А. Лейкину. 25 января 1886 г. Москва'] = '28 января 1886 г. Москва'
    dates_info['Чехов -- А. С. Суворину. 30 августа 1891 г. Вогимово'] = '30 августа 1891 г. Богимово'
    dates_info['Чехов -- А. С. Суворину. 27 март 1Я94 г. Ялта'] = '27 марта 1894 г. Ялта'
    dates_info['Чехов -- А. С. Суворину. 21 октября 1895 г. Мелихова'] = '21 октября 1895 г. Мелихово'
    dates_info['Чехов -- А. С. Суворину. 6 (18) февраля 1898 г. Ницца'] = '6(18) февраля 1898 г. Ницца'
    dates_info['Чехов -- В. Г. Короленко. 2 мая 1888 г. Москва'] = '2 мая 1883 г. Москва'
    dates_info['В. Г. Короленко -- Чехову. 4 августа 1902 г. Джанхот'] = '4 августа 1902 г, Джанхот'
    dates_info['А. Н. Плещеев -- Чехову. 30 марта 1888 г. Петербург'] = '30 марта 188S г. Петербург'
    dates_info['А. Н. Плещеев -- Чехову. 5 ноября 1889 г. Петербург'] = '5 ноября 1889 г, Петербург'
    dates_info['Чехов -- Я. П. Полонскому, 25 марта 1888 г. Москва'] = '25 марта 1888 г. Москва'

    return cutted_text, dates_info


def letters_split(cutted_text, dates_info):
    starts = []
    for date in dates_info.values():
        improved_date = date.replace('(', '\(').replace(')', '\)')
        starts_date = [(match.start(), len(date)) for match in re.finditer(improved_date, cutted_text)]
        starts += starts_date
    starts.sort()
    maybe_letters = [cutted_text[starts[i][0] + starts[i][1]: starts[i + 1][0]] for i in range(len(starts) - 1)]
    maybe_letters.append(cutted_text[starts[-1][0] + starts[-1][1]:])

    letters = [letter for letter in maybe_letters if len(letter) > 10]
    return letters


def remove_spaces(letters):
    for i in range(len(letters)):
        letters[i] = letters[i].strip()
        letters[i] = '\n'.join(letters[i].split('\n')[: -1]).strip()


def remove_autograph(letters):
    pattern_pages = '(с\. (\d+(--|-)\d+))|(ГБЛ)|(Печатается по автографу)|(т. \d+, No \d+)'
    for i in range(len(letters)):
        strings = letters[i].split('\n')
        min_bad_idx = len(strings)
        for idx, string in enumerate(strings):
            if re.search(pattern_pages, string):
                min_bad_idx = idx
                break
        strings = strings[: min_bad_idx]
        letters[i] = '\n'.join(strings).strip()


def remove_first_empty_strings(letters):
    for i in range(len(letters)):
        strings = letters[i].split('\n')
        if len(strings) >= 2 and len(re.findall('\d+', strings[0])) > 0 and strings[1] == '':
            letters[i] = '\n'.join(strings[1:]).strip()


def remove_invalid_symbols(letters):
    pattern = '[а-яА-ЯёЁ\(\)"]+\d+[\.,!?]*'
    for i in range(len(letters)):
        words = letters[i].split()
        for j in range(len(words)):
            if re.match(pattern, words[j]):
                idx = 0
                while not words[j][idx].isdigit():
                    idx += 1
                new_word = words[j][: idx]
                if not words[j][-1].isdigit():
                    new_word += words[j][-1]
                letters[i] = letters[i].replace(words[j], new_word)


def get_letters(url, outfile='chekhov.pkl'):
    text = get_whole_text(url)
    cutted_text, dates_info = find_dates(text)
    letters = letters_split(cutted_text, dates_info)

    remove_spaces(letters)
    remove_autograph(letters)
    remove_first_empty_strings(letters)
    remove_invalid_symbols(letters)

    with open(outfile, 'wb') as f:
        pickle.dump(letters, f)


if __name__ == '__main__':
    url = 'http://az.lib.ru/c/chehow_a_p/perepiska_tom1.shtml'
    get_letters(url)
