import requests  # Импорт модуля для работы с requets'ами
import bs4  # Импорт модуля для работы с парсингом
import re  # Для работы с регулярными выражениями

# from bs4 import BeautifulSoup - можно заменить на импорт через from, тогда
# сможешь работать по короткому имени BeautifulSoup


def get_news(p_name):
    ''' На вход принимаем url-адрес страницы, возвращаем список словарей со следующими данными:
        ключ        :   значение
        ============================
        author      :   автор новости
        comments    :   количество комментариев
        points      :   оценки (лайки)
        title       :   заголовок новости
        url         :   ссылка на новость '''
    try:
        req = requests.get(p_name)  # Формируем запрос на страницу, переданную нам в атрибутах фукнции
        if req.status_code == 200:
            pass
        else:
            print('Status: False, status code:', req.status_code)
            return []
    except requests.exceptions.MissingSchema:  # Если url не проходит проверку - возвращаем пустой список
        print('Missing Schema - check URL-address')
        return []
    except requests.exceptions.ConnectionError:  # Не можем соеденится по указанному адресу (Опять же, битый URL)
        print('Connect error - check URL-address')
        return []
    except:  # Любые остальные исключения - думай, что нужно обрабатывать, что нет
        print('Something wrong')
        return []

    # Опять же - прикинь, устроит ли тебя такой выход по ошибкам - т.е. return пустого списка в случае исключения
    # Тут можно посоветоваться с мамкой-папкой, как это дело обрабатывать в плюсах.
    # Сюда мы выходим с req.status_code = 200 (т.е. мы получили какую-то страницу
    p = bs4.BeautifulSoup(req.text, 'html.parser')  # Создаем суп из полученного нами запроса страницы
    tbl_list = p.table.findAll('table')  # Тут ты сидишь и анализируешь html-код страницы. Часть есть в методичке
    tr_ath = tbl_list[1].findAll('tr', {'class': 'athing'})  # Мне было удобнее создавать два тэга, можно через один
    td_sub = tbl_list[1].findAll('td', {'class': 'subtext'})

    news_list = []  # Пустой список - в него будем добавлять словари

    for i in range(len(tr_ath)):  # Для каждого элемента тэга

        try:  # Пробуем получить заголовок новости
            tit = tr_ath[i].find('a', {'class': 'storylink'}).string
        except:  # Если что-то не получается - говорим, что заголовка нет
            tit = None

        try:  # Пробуем получить url-ссылку на новость
            url = tr_ath[i].find('a', {'class': 'storylink'})['href']
        except:
            url = None

        try:  # Пробуем получить автора новости
            author = td_sub[i].find('a', {'class': 'hnuser'}).string
        except:
            author = None

        try:  # Пробуем получить оценки
            points = int(td_sub[i].find('span', {'class': 'score'}).string.split()[0])
        except:
            points = 0

        try:  # Здесь немного тяжело читаемая хрень. Комментарии лежат в тэге a и у них нет ни класса, нифига.
              # Через регулярку их тоже не отловить, т.к. выше есть a c herf'ом, начинающимся также
              # Что делаем - берем все тэги а, из них берем последний, смотрим его строку - если в конце comment - это оно
            comments = td_sub[i].findAll('a')
            z = comments[len(comments)-1].string.split()
            if z[1][:7] == 'comment':
                comments = int(z[0])
            else:
                comments = 0
        except:
            comments = 0

        news_list.append({'author': author, 'comments': comments, 'points': points, 'title': tit, 'url': url})
    return news_list