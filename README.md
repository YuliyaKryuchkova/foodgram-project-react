# Foodgram

_Социальная сеть кулинарный помощник, в котором можно создавать рецепты,
добавлять в избранное понравившиеся, на основе выбраных рецептов формируется список необходимых продуктов,
который можно скачать. Так же можно подписываться и отписываться от авторов понравившихся вам своими рецептами.
Стек технологий: Python 3.8, Django 2.2.19, Яндекс.Облако, PostgreSQL, Gunicorn, Nginx, Docker._
### Как запустить проект:

* Форкните репозиторий и перейдите в него в командной строке:

```
https://github.com/YuliyaKryuchkova/foodgram-project-react
```

### Установка Docker

* Установка Windows Subsystem for Linux (WSL):

По инструкции с официального сайта Microsoft.
https://learn.microsoft.com/ru-ru/windows/wsl/install

* После установки WSL: 

установите Docker на Windows
Зайдите на официальный сайт проекта и скачайте установочный файл Docker Desktop.
https://www.docker.com/products/docker-desktop/

* Установка Docker на Linux

1) Установка Docker на Linux — скачайте и выполните официальный скрипт.
https://docs.docker.com/engine/install/ubuntu/#install-using-the-convenience-script
Для этого поочерёдно выполните в терминале следующие команды:

`sudo apt update
`
`sudo apt install curl
` 
2) С помощью утилиты curl скачайте скрипт для установки докера с официального сайта.

`curl -fSL https://get.docker.com -o get-docker.sh
`
3) Запустите сохранённый скрипт с правами суперпользователя:

`sudo sh ./get-docker.sh
`
* Дополнительно к Docker установите утилиту Docker Compose:
 
`sudo apt-get install docker-compose-plugin
`
* Проверьте, что Docker работает:

`sudo systemctl status docker
`
* Установка Docker на macOS
Зайдите на официальный сайт проекта https://www.docker.com/products/docker-desktop/ и скачайте установочный файл Docker Desktop для вашей платформы — Apple Chip для процессоров M1/M2 и Intel Chip для процессоров Intel.
Откройте скачанный DMG-файл и перетащите Docker в Applications, а потом — запустите программу Docker.


### Упаковка проекта в Docker-образ

* Форкните и клонируйте локально себе на компьютер репозиторий 
https://github.com/YuliyaKryuchkova/foodgram-project-react
* Перейдите в директорию cd infra

* Создайте папку .env, перенесите в нее список (указав свои данные) из файла .env.example

### Установка docker compose на сервер:

`sudo apt update`

`sudo apt install curl`

`curl -fSL https://get.docker.com -o get-docker.sh`

`sudo sh ./get-docker.sh`

sudo apt-get install docker-compose-plugin

* В директорию infra/ скопируйте файлы docker-compose.production.yml и .env:

`scp -i path_to_SSH/SSH_name docker-compose.production.yml username@server_ip
`
1) path_to_SSH — путь к файлу с SSH-ключом;

2) SSH_name — имя файла с SSH-ключом (без расширения);

3) username — ваше имя пользователя на сервере;

4) server_ip — IP вашего сервера.

* Запустите docker compose в режиме демона:

sudo docker compose -f docker-compose.production.yml up -d

* Выполните миграции, соберите статические файлы бэкенда и скопируйте их в /backend_static/static/ Пошагово выполните команды:

            sudo docker compose -f docker-compose.production.yml down

            sudo docker image rm yuliyakryuchkova/foodgram_backend

            sudo docker compose -f docker-compose.production.yml up -d

            sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate

            sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic --noinput

Файл workflow уже написан. Он находится в директории foodgram-project-react/.github/workflows/main.yml

* Добавьте секреты в GitHub Actions:

DOCKER_USERNAME                # имя пользователя в DockerHub

DOCKER_PASSWORD                # пароль пользователя в DockerHub

HOST                           # ip_address сервера

USER                           # имя пользователя

SSH_KEY                        # приватный ssh-ключ (cat ~/.ssh/id_rsa)

SSH_PASSPHRASE                 # кодовая фраза (пароль) для ssh-ключа

TELEGRAM_TO                    # id телеграм-аккаунта (можно узнать у @userinfobot)

TELEGRAM_TOKEN                 # токен бота (получить токен можно у @BotFather)

* Коммитим и пушим изменения на GitHub.

` git add .`

` git commit -m 'твой коммит'`

` git push`


### Автор:

@YuliyaKryuchkova

