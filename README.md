# Reviews Rest API with oauth2 authentication

Rest backend for manage review and comment to him.
Used oauth2 authentication, for access use http client (curl, http)

## Requirements

python 
postgres 
Nginx
uWSGI
virtualenv

## Installation
clone this project to `/var/www` dir with:
```shell
    git clone https://github.com/Feuermann/review.git
```
You, should grant all important access. 
Prepare your environment, if you need, install virtualenv

```shell
    virtualenv --no-site-packages -p /usr/bin/python3 venv
```

where `-p /usr/bin/python`  path to your python interpreter

next activate your virtualenvironment

```shell
    source venv/bin/activate 
```

go to project dir and install requirements packages.

```shell
    pip install -r requirements.txt
```

next you need apply migrations to database,
For first, you should create user and create database and grant access
 to this database for user. <br>
 Write database data to `postgres.conf` in dir `configs`.
 After this run:

```shell
    python manage.py migrate
```
where `manage.py` - manage file in project dir or path to this file

and next run project with web server
 
copy config to nginx with
 
```shell
    cp configs/review_nginx.conf /etc/nginx/sites-available
    ln -s /etc/nginx/sites-available/review_nginx.conf /etc/nginx/sites-enabled/
``` 

reload nginx

```shell
    /etc/init.d/nginx restart
```

and after then, run uWSGI:

```shell
    uwsgi --ini configs/uwsgi.ini
```
## Usage
    
    Use console agent to connect to API,
    
For sign-Up need create user profile, you should send username 
and password, for `http://localhost:8000/sign_up/`

```shell
    curl -X POST http://localhost:8000/sign_up/ -d '{"username":"user","password":"password"}' -H 'Content-Type: application/json'
```

for sign_in send username and password to `http://localhost:8000/sign_in/` url

```shell
    curl -X POST http://localhost:8000/sign_in/ -d '{"username":"user","password":"password"}' -H 'Content-Type: application/json'
```

and you receive responce with your token, add token to header, and you will have access to API

