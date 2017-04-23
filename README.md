# Reviews Rest API with oauth2 authentication

Rest backend for manage review and comment to him.
Used oauth2 authentication, for access use http client (curl, http)

[Requirements](#requirements)   <br>
[Installation](#installation)   <br>
[Autodeployement](#autodeployement)<br>
[Manual installation](#manual-installation) <br> 
[Usage](#usage) <br>
[Sign Up](#sign-up)<br>
[Sign In](#sign-in)<br>
[Review](#review)<br>
[Create review](#create-review)<br>
[Create comment](#create-comment)<br>
[List all review](#list-all-review)<br>


## Requirements

python 
postgres 
Nginx
uWSGI
virtualenv

## Installation

### autodeployement
>For autodeployment you must have installed `ansbile`, if he is not installed run:
```shell
  apt-get install ansible
```


For use autodeployment follow next step:

* clone this project to `/var/www` dir with:
```shell
    cd /var/www
    git clone https://github.com/Feuermann/review.git
```
You, should grant all important access. 

* At begin run:
```shell
    ansible-playbook install.yml
```
* Then create database with `reviews` name (if your user haven't permission to create db), and create user (use `postgres` user is a bad idea)
and write database credentials to `configs/postgres.conf`

* Next run
```shell
    ansible-playbook setup.yml
```

Congrats. Project deployed and configured.

run in project dir
~~~shell
    ./run.sh
~~~

Project work. [Next](#usage)


### Manual installation

For manual installation follow next step:

clone this project to `/var/www` dir with:
```shell
    cd /var/www
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

#### Sign Up
    
For sign-Up need create user profile, you should send username 
and password, for `http://localhost:8000/sign_up/`

```shell
    curl -X POST http://localhost:8000/sign_up/ -d '{"username":"user","password":"password"}' -H 'Content-Type: application/json'
```

#### Sign In

for sign_in send username and password to `http://localhost:8000/sign_in/` url

```shell
    curl -X POST http://localhost:8000/sign_in/ -d '{"username":"user","password":"password"}' -H 'Content-Type: application/json'
```

#### Review

and you receive responce with your token, add token to header, and you will have access to API
response example:
```shell
    {"token_type":"Bearer","refresh_token":"I7ihmXhGqger1TCgZUImhdwUexEtHF","expires_in":36000,"access_token":"AV2OPVN6w4m33pYl0VBR0GwOcIV1RK","scope":"groups write read"}
```

call to review page to get all review with comment

```
     curl -H 'Authorization: Bearer AV2OPVN6w4m33pYl0VBR0GwOcIV1RK' http://127.0.0.1:8000/review/
```

#### create review
you should send request to `/review` with review data, as 
 * title - title your review
 * text - text your review
 * author - user id
 
```
    curl -H 'Authorization: Bearer AV2OPVN6w4m33pYl0VBR0GwOcIV1RK' -H 'Content-Type: application/json' -X POST -d '{"title":"new review", "text":"New review for example","author":1}'  http://127.0.0.1:8000/review/

```

#### create comment
you should send request to `/comment` with review data, as 
 * author - author's id
 * text - text your comment
 * review - review's id for add comment
 
 ```
    curl -H 'Authorization: Bearer AV2OPVN6w4m33pYl0VBR0GwOcIV1RK' -H 'Content-Type: application/json' -X POST -d '{"review":1, "text":"Add example comment for example review #1","author":1}'  http://127.0.0.1:8000/comment/
 ```
 
 #### list all review
 
 ```
         curl -H 'Authorization: Bearer AV2OPVN6w4m33pYl0VBR0GwOcIV1RK' http://127.0.0.1:8000/review/
 ```
 
 and you receive all review with comments, for example:
  
```javascript
    {"count":1,"next":null,"previous":null,"results":
        [{"id":1,"comments":[
            {"id":1,"created_at":"2017-04-23T12:39:44.669782Z","updated_at":"2017-04-23T12:39:44.669839Z","text":"Add example comment for example review #1","author":1,"review":1},
            {"id":2,"created_at":"2017-04-23T12:42:49.294246Z","updated_at":"2017-04-23T12:42:49.294296Z","text":"Add example comment for example review #2","author":1,"review":1},
            {"id":3,"created_at":"2017-04-23T12:42:53.972745Z","updated_at":"2017-04-23T12:42:53.972794Z","text":"Add example comment for example review #3","author":1,"review":1}],
        "created_at":"2017-04-23T12:35:06.043710Z","updated_at":"2017-04-23T12:35:06.043759Z","title":"new review","text":"New review for example","author":1}]}
```

result are paginated by 10 entries, for receive next result page run

 ```
         curl -H 'Authorization: Bearer AV2OPVN6w4m33pYl0VBR0GwOcIV1RK' http://127.0.0.1:8000/review/?page=2
 ```
 
#### update/delete

You can update/delete entries in accordance with request,
PATCH/DELETE for update/delete entry.

