from data import db_session
from data import users
from data import news
from data import categories
import datetime
import os

def clear_file(file_name):
    file = open(file_name, 'w')
    file.write("")
    file.close()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_path = BASE_DIR + "/db/blog.sqlite"
clear_file(db_path)
db_session.global_init(db_path)

# Создание пользователей
session = db_session.create_session()
user1 = users.User(login="vvp", password="12345", name="Владимир Владимирович")
session.add(user1)
session.commit()


# Получение объекта-пользователя
user1 = session.query(users.User).filter(users.User.login == "vvp").one()

#создание объекта-категории
category1 = categories.Category(name="kjdfsnosjnfo")
session.add(category1)
session.commit()

#получение объекта-категории
category1 = session.query(categories.Category).filter(categories.Category.name == "kjdfsnosjnfo").one()

# Добавление новостей
news1 = news.News(title="Ура!", content="Нового года не будет", user_id=user1.id, name_of_category=user1.login, data='1')
news2 = news.News(title="Снова ура!", content="Пасхи не будет!", user_id=user1.id, name_of_category=user1.login, data='1')
session.add(news1)
session.add(news2)
session.commit()


# Получение всех новостей, созданных пользователем
user1 = session.query(users.User).filter(users.User.login == "vvp").one()
user_news = session.query(news.News).filter(news.News.user_id == user1.id)
for NEWS in user_news:
    print(NEWS.title)
    print(NEWS.content)
    print("-" * 20)


# Удаление пользователя (с каскадным удалением принадлежащих ему новостей)
user1 = session.query(users.User).filter(users.User.login == "vvp").one()
session.delete(user1)
session.commit()

def main():
    global user1
    print("Привет")
    print("выбор")
    _quit = False
    while not _quit:
        command = input()
        if command == "Добавить Категорию":
            new_category_name = input()
            category1 = session.query(categories.Category).filter(categories.Category.name == new_category_name).one()
            if category1 is None:
                session.add(category1)
                print("Новая категория добавлена")
                session.commit()
            else:
                print("Такая категория уже существует")
        elif command == "Добавить Заметку":
            print("Введите имя категории, к которой относится данная заметка")
            category_name = input()
            category1 = session.query(categories.Category).filter(categories.Category.name == category_name).one()
            if category1 is not None:
                print("Введите название заметки")
                name_of_news = input()
                print("Введите сожержимое заметки")
                input_of_news = input()
                d = datetime.datetime.now()
                str_time = str(d)
                news_1 = news.News(title=name_of_news, content=input_of_news, user=user1, name_of_category=category_name, data=str_time)
                session.add(news_1)
                session.commit()
            else:
                print("Такой категории не существует")
        elif command == "Просмотреть все заметки с определенной категорией":
            user_category = input()
            category1 = session.query(categories.Category).filter(categories.Category.name == user_category).one()
            if category1 is not None:
                news_list = session.query(news.News).filter(news.News.name_of_category == user_category).all()
                for NEWS in news_list:
                    print(NEWS.data, NEWS.title, '\n', NEWS.content)
            else:
                print("Такой категории не существует")
        elif command == "Поиск по содержимому заметок":
            user_find = input()
            need_news = session.query(news.News).filter(news.News.content.like("%" + user_find + "%"))
            for NEWS in need_news:
                print(NEWS.data, NEWS.title, '\n', NEWS.content)
        elif command == "Просмотр заметок в определенный интервал времени":
            print("Введите старт время")
            user_data1 = input()
            print("Введите конечное время")
            user_data2 = input()
            news_list = session.query(news.News).filter(news.News.data > user_data1, news.News.data == user_data1, news.News.data < user_data2, news.News.data == user_data2)
            for NEWS in news_list:
                print(NEWS.data, NEWS.title, '\n', NEWS.content)
        elif command == "Удалить заметку":
            print("Введите дату добавления заметки")
            user_data = input()
            user_news = session.query(news.News).filter(news.News.data == user_data).one()
            if user_news is not None:
                session.delete(user_news)
                session.commit()
                print("Заметка удалена")
            else:
                print("Такой заметки уже не существует")
        elif command == "Удалить категорию":
            print("Введите название категории")
            name_category = input()
            user_category = session.query(categories.Category).filter(categories.Category.name == name_category).one()
            if user_category is not None:
                news_list = session.query(news.News).filter(news.News.name_of_category == name_category).all()
                for NEWS in news_list:
                    session.delete(NEWS)
                    session.commit()
                session.delete(user_category)
            else:
                print("Такой категории уже не существует")
        elif command == "quit":
            _quit = True
            print("До свидания")
        else:
            print("Команда не распознана")
main()