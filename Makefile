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