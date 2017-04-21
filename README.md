# Reviews Rest API with oauth2 authentication

Rest backend for manage review and comment to him.
Used oauth2 authentication, for access use http client (curl, http)

## Requirements

python >= 3.5

## Installation
clone this project with
```shell
    git clone https://github.com/Feuermann/review.git
```
prepare your environment, if you need, install virtualenv

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

next you need apply migrations to database, run:

```shell
    python manage.py migrate
```
where `manage.py` - manage file in project dir or path to this file

and next run project with any web server
 
## Usage