# Проект Foodgram
Сайт Foodgram, «Продуктовый помощник».
Онлайн-сервис и API для него. На этом сервисе пользователи после регистрации могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

![example workflow](https://github.com/iurij-n/foodgram-project-react/actions/workflows/foodgram.yml/badge.svg)

IP сервера - 178.154.195.175

Всё это можно видеть в сборе:

админка (login: admin, password: admin) - <http://178.154.195.175/admin/>

API - <http://178.154.195.175/api/>

Документация API - <http://178.154.195.175/api/docs/>


### Технологии
- Python 3.7
- Django 3.2.13
 - Gunicorn
 - Nginx
 - Docker
 - PostgreSQL
# Шаблон наполнения env-файла

    SECRET_KEY=<seckret_key>
    ALLOWED_HOSTS=<allowed HOSTs>
    DB_ENGINE=django.db.backends.postgresql
    DB_NAME=<The name of the database, for example 'postgres'>
    POSTGRES_USER=<Database user name, for example "postgres">
    POSTGRES_PASSWORD=<Database user password>
    DB_HOST=db
    DB_PORT=5432

# Запуск приложения в контейнерах
1. Клонируйте проект
```
https://github.com/iurij-n/foodgram-project-react.git
```
2. Перейдите в папку infra, создайте файл .env по шаблону (.env.template) и разверните контейнеры
```
docker-compose up -d --build
```
3. Создайте миграции
```
docker-compose exec backend python manage.py makemigrations
```
4. Выполните миграции
```
docker-compose exec backend python manage.py migrate
```
5. Соберите статику
```
docker-compose exec backend python manage.py collectstatic --no-input
```
6. Наполните базу данных тестовыми данными
```
docker-compose exec backendb python manage.py loaddata fixtures.json
```

### Автор

Юрий Новиков

mail:  [iurij.novickov2016@yandex.ru](mailto:iurij.novickov2016@yandex.ru); 
Telegram:  [https://t.me/Jurij_7](https://t.me/Jurij_7)

