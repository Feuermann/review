apt-get install -y python-pip python-dev libpq-dev postgresql postgresql-contrib
apt install -y python3.5-dev
apt install -y virtualenv

virtualenv --no-site-packages -p /usr/bin/python3 venv

source venv/bin/activate

pip install -r requirement.txt

cp configs/review_nginx.conf /etc/nginx/sites-available/

ln -s /etc/nginx/sites-available/review_nginx.conf /etc/nginx/sites-enabled/

/etc/init.d/nginx restart

python manage.py migrate

python manage.py collectstatic

uwsgi --ini configs/uwsgi.ini