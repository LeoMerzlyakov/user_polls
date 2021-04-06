# User_polls
### Описание
API для создания и проведения опросов.
### Технологии
- Python 3.8.5
- Django 2.2.10
- djangorestframework 3.12.4
- drf-yasg==1.20.0
### Запуск проекта в dev-режиме
- скопируйте проект в нужную директорию
```
git clone https://github.com/LeoMerzlyakov/user_polls.git
```

- Установите и активируйте виртуальное окружение
```
python -m venv venv
```

- Запустите виртуальное окружение
```
. venv/Scripts/activate
```

- Установите зависимости из файла requirements.txt
```
pip install -r requirements.txt
```

- В папке с файлом manage.py выполните команду:
```
python3 manage.py runserver
```

### Документация по API
    http://127.0.0.1:8000/swagger/