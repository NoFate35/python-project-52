build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi

install:
	uv sync

collectstatic:
	django-admin collectstatic

migrate:
	uv run manage.py migrate