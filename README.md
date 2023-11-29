# Flask-App
[![Test and Build](https://github.com/rodzera/flask-app/actions/workflows/test_and_build.yml/badge.svg?branch=master)](https://github.com/rodzera/flask-app/actions/workflows/test_and_build.yml) [![Python 3.11](https://img.shields.io/badge/python-3.11.x-blue.svg)](https://www.python.org/downloads/release/python-3111/) [![flask](https://img.shields.io/badge/flask-3.0.x-blue.svg)](https://flask.palletsprojects.com/en/3.0.x/)

A flask app structure with the following features:

- RESTful API with [marshmallow](https://flask-marshmallow.readthedocs.io/en/latest/) validation
- Users and roles [SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/) models
- [PostgreSQL](https://hub.docker.com/_/postgres) and [MySQL](https://hub.docker.com/_/mysql) support
- [Migrations](https://flask-migrate.readthedocs.io/en/latest/) versioning
- Runtime [logging](https://docs.python.org/3.11/library/logging)
- Unittests with [Pytest](https://docs.pytest.org/en/7.4.x/)
- [Swagger](https://github.com/flasgger/flasgger) documentation
- [Docker Hub](https://docs.docker.com/docker-hub/) deployment
- CI/CD pipelines with [GitHub Actions](https://docs.github.com/en/actions)
- Production-ready [Docker Compose](https://docs.docker.com/compose/) setup with [Gunicorn](https://gunicorn.org/)

##### Feel free to use or modify this project :)

## Requirements

- Create a python3.11 venv within the project's root directory and set up the environment:

```shell
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt install -y python3.11 python3.11-dev python3-venv
python3.11 -m venv venv
. venv/bin/activate
pip install -r src/requirements.txt
```

- Export the following environment variables (modify the values as needed):

```shell
export _ADMIN_PASS=admin
export _SECRET_KEY=ABCDEFGH12345678
export _DB_PROVIDER=postgresql
export _DB_DATABASE=db
export _DB_HOST=172.17.0.2
export _DB_PASS=admin
```

- Sample of a PostgreSQL and MySQL databases using docker:

```shell
# postgres
docker run -dit \
--name flask-app-database \
-p 5432:5432 \
-e POSTGRES_DB=flask-app \
-e POSTGRES_USER=admin \
-e POSTGRES_PASSWORD=admin \
postgres:latest

# mysql
docker run -dit \
--name flask-app-database \
-p 3306:3306 \
-e MYSQL_DATABASE=flask-app \
-e MYSQL_USER=admin \
-e MYSQL_PASSWORD=admin \
-e MYSQL_RANDOM_ROOT_PASSWORD=True \
mysql:latest
```

## Migrations

Before starting the application it is essential to upgrade the database to the latest migration version and populate it with the default user/admin roles. Within the `src` directory:

- Upgrade database: `flask db upgrade`
- Populate database: `flask populate_roles`

## Running

- Development mode: `flask --debug --app src.app -h 0.0.0.0 -p 8080`
- Production mode: `gunicorn --bind 0.0.0.0:8080 --threads 64 --worker-class gthread --workers 4 --worker-connections 8192 "src.app"`

### Docker Compose

To run the application with docker compose, follow these steps within the `docker-compose` directory:

* Rename the `template.env` file to `.env` and fill the variables with real values
* Run `docker compose up`

Optionally, you can build a local docker image by running `make` within the `src` directory.

## Testing

- Within the project's root directory:

```shell
export _TESTING=1
python3 -m pytest src/tests/unittests
```

## Documentation

- Swagger: `http://0.0.0.0:8080/apidocs`
