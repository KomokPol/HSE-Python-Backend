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

load_fixtures:
	$(PYTHON3) manage.py loaddata mock_data

build_docker:
	docker build -t django-backend .

run_docker:
	docker run -d -p 8000:8000 --name django-backend django-backend

stop_docker:
	docker stop django-backend
	docker rm django-backend
