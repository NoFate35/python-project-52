build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi

install:
	uv sync

collectstatic:
	uv run manage.py collectstatic --noinput

migrate:
	uv run manage.py migrate
start:
	git pull
	sudo service postgresql start
	uv run manage.py runserver
test:
	uv run python3 manage.py test task_manager.statuses.tests