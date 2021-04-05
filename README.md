# Описание

Тестовое задание

## Установка

git init

git clone <https://github.com/TolstochenkoDaniil/imageapp.git> .

Настройка окружения

```sh
python -m venv env

source env/scripts/activate

pip install -r requirements.txt
```

Запуск проекта

```sh
cd imageapp

python manage.py makemigrations

python manage.py migrate --run-syncdb

python manage.py runserver 7000
```

## Тесты

Запуск всех тестов

```sh
py.test
```
