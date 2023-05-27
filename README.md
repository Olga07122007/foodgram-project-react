# praktikum_new_diplom

Проект «Продуктовый помощник». Онлайн-сервис и API для него. На этом сервисе пользователи могут публиковать рецепты, 
подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», 
а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного 
или нескольких выбранных блюд.  
  
Проект разворачивается в Docker контейнерах (nginx, PostgreSQL и Django) 
(контейнер frontend используется лишь для подготовки файлов) через docker-compose на сервере в Яндекс.Облаке. 
Образ с проектом запушен на Docker Hub.  
  
  
## Стек технологий

![python version](https://img.shields.io/badge/Python-3.7-yellowgreen) 
![python version](https://img.shields.io/badge/Django-3.2-yellowgreen) 
![python version](https://img.shields.io/badge/djangorestframework-3.12.4-yellowgreen) 
![python version](https://img.shields.io/badge/djoser-2.1.0-yellowgreen) 
![python version](https://img.shields.io/badge/PostgreSQL-yellowgreen)
![python version](https://img.shields.io/badge/Nginx-yellowgreen)
![python version](https://img.shields.io/badge/gunicorn-yellowgreen)
![python version](https://img.shields.io/badge/Docker-yellowgreen)
![python version](https://img.shields.io/badge/DockerHub-yellowgreen)
![python version](https://img.shields.io/badge/JS-yellowgreen)
![python version](https://img.shields.io/badge/GitHub-Actions-F7DF1E)

## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Olga07122007/foodgram-project-react.git
cd foodgram-project-react/
cd infra/
```

В директории `infra/` создать файл `.env`, согласно примеру:

```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```


## Запустить приложение в контейнерах:

*из директории `infra/`*
```
docker-compose up -d --build
```

Выполнить миграции:

*из директории `infra/`*
```
docker-compose exec backend python manage.py migrate
```

Создать суперпользователя:

*из директории `infra/`*
```
docker-compose exec backend python manage.py createsuperuser
```

Собрать статику:

*из директории `infra/`*
```
docker-compose exec backend python manage.py collectstatic --no-input
```

## Заполнить БД тестовыми данными

Для заполнения базы использовать файл `ingredients.json`, в директории `backend/data`. Выполните команду:

*из директории `infra/`*
```
docker-compose exec backend python manage.py load_ingredients ingredients.json
```


### Адресa:
Проект доступен по адресу: http://158.160.5.17/  
Админка Django: http://158.160.5.17/admin/
