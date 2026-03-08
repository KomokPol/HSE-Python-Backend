PIP := venv/Scripts/pip
PYTHON3 := venv/Scripts/python

clear:
	python -c "import shutil; shutil.rmtree('venv', ignore_errors=True)"

venv:
	python -m venv venv

install_requirements:
	$(PIP) install -r requirements.txt

freeze:
	$(PIP) freeze > requirements.txt

run:
	$(PYTHON3) manage.py runserver

create_migrations:
	$(PYTHON3) manage.py makemigrations

migrations:
	$(PYTHON3) manage.py migrate

up_service:
	make venv
	make install_requirements
	make create_migrations
	make migrations
	make run

superuser:
	$(PYTHON3) manage.py createsuperuser

test:
	python manage.py test backend

compose_up:
	docker-compose up --build

compose_down:
	docker-compose down
