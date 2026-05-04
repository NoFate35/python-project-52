### Hexlet tests and linter status:
[![Actions Status](https://github.com/NoFate35/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/NoFate35/python-project-52/actions)

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=NoFate35_python-project-52&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=NoFate35_python-project-52)

## Skill badges
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Pytest](https://img.shields.io/badge/pytest-%23ffffff.svg?style=for-the-badge&logo=pytest&logoColor=2f9fe3)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)


# About project
The link to this training project will be available for 25 days, starting from 20/04/2026: <a href="https://python-project-52-4mns.onrender.com">Task manager</a>
### Purpose
Practicing database management and website development using the django framework
### Description
<a href="https://python-project-52-4mns.onrender.com">Task manager</a> – this is a task management, similar to <a href="http://www.redmine.org">Remine</a>: It allows you to set tasks, assign executors, and change their statuses. Registration and authentication are required to use the system.

### Installation
To work with the project must be installed:
* the __uv__ project manager;
* __postgresql__ database;

__.env__ file consist of (like):
```
DATABASE_URL = 'postgresql:///py_flaskdb'
SECRET_KEY = 'verysecretkeyyy'
ALLOWED_HOSTS = 'webserver, localhost'
```
then:
```
git clone https://github.com/NoFate35/python-project-52.git
cd python-project-52
make install
make migrate
make test
```



