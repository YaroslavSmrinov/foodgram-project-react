# Foodgram: «Продуктовый помощник»

«Продуктовый помощник» - это сайт, на котором можно поделиться рецептом с другими, взять на заметку что-то новое, зафоловить любимых поваров. 
А кнопка "Список покупок" поможет понять, что и сколько нужно будет купить.

Проект доступен по [адресу](http://158.160.5.58/)
[Админка сайта](http://158.160.5.58/admin/)
Креды для теста админки: admin@mail.ru admin

## Технологии:
+ Django 3
+ psycopg2-binary
+ Pillow
+ DRF 3
+ React.JS
    > на js не писал, платформа предоставила
+ Docker-compose

## Установка
Клонируем репозиторий
```
git@github.com:YaroslavSmrinov/foodgram-project-react.git
```
Переходим в необходимую директорию 
```
cd foodgram-project-react/infra/
```
Запускаем сборку 
```
docker compose up -d --build
```
После сборки и запуска появится 3 контейнера: postgres, nginx, backend.
В контейнере backend применим миграции, подтянутся все возможные ингредиенты.
```
docker compose exec backend python manage.py migrate
```
Подтянем статику
```
docker compose exec backend python manage.py collectstatic
```
Готово!

## АДМИН ЗОНА

Для теста админки выполним команду
```
docker compose exec backend python manage.py createsuperuser
```
Переходим по [адресу](http://158.160.5.58/admin/)

## Об авторах
Backend: @irs_sm
Frontend: [Яндекс.Практикум](https://practicum.yandex.ru/profile/python-developer-plus/)