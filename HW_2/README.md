# Flask-проект


Небольшой проект на Flask. В репе есть простой сервер на Flask с маршрутами:
- `/` - простой ответ "My server"
- `/author` - JSON с информацией об авторе
- `/sum` - складывает переданные числа через GET-параметры `a` и `b`


Инструкции по запуску:
1. Создать виртуальное окружение: `python -m venv venv`
2. Активировать: Windows: `venv\Scripts\activate`, Linux/macOS: `source venv/bin/activate`
3. Установить зависимости: `pip install -r requirements.txt`
4. Запустить: `python server.py` или `make run`


Запуск тестов:
- `make test`