# Flask-App
[![Test and Build](https://github.com/rodzera/flask-app/actions/workflows/test_and_build.yml/badge.svg?branch=master)](https://github.com/rodzera/flask-app/actions/workflows/test_and_build.yml)

A flask app template. Feel free to use or modify :)

```json
 {
    "name": "flask-app",
    "version":  "1.0.0",
    "developer": "github.com/rodzera",
    "tech_stack": {
        "python": "3.11",
        "frameworks": [
            "flask"
        ],
        "libraries": [
            "sqlalchemy",
            "flask-migrate",
            "marshmallow",
            "swagger",
            "gunicorn",
            "werkzeug"
        ],
        "databases": [
            "sqlite",
            "mysql",
            "postgres"
        ],
        "tests": [
            "unittests"
        ],
        "ci/cd": [
            "github actions"
        ],
        "devops": [
            "docker"
        ]
    }
}
```

## Requirements

- Create a python3.11 venv inside the project's root directory and set up the environment:

```shell
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt install -y python3.11 python3.11-dev python3-venv
python3 -m venv venv
. venv/bin/activate
pip install -r src/requirements.txt
```

- Export the following env variables:

```shell
export _ADMIN_PASS=admin
export _SECRET_KEY=ABCDEFGH12345678
export _DB_PROVIDER=postgresql
export _DB_DATABASE=db
export _DB_HOST=172.17.0.2
export _DB_PASS=admin
```

- Sample of a postgres database with docker:

```shell 
docker run -dit \
--name database \
-p 5432:5432 \
-e POSTGRES_DB=db \
-e POSTGRES_USER=admin \
-e POSTGRES_PASSWORD=admin \
postgres:latest
```

## Running

- Development mode: `flask --debug --app src.app -h 0.0.0.0 -p 8080`
- Production mode: `gunicorn --bind 0.0.0.0:8080 --threads 64 --worker-class gthread --workers 4 --worker-connections 8192 "src.app"`

## Testing

- Inside the project's root directory:

```shell
export _TESTING=1
python3 -m unittest discover -s src/tests -t src
```

## Documentation

- Swagger: `http://127.0.0.1:8080/apidocs`
