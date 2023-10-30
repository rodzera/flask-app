from os import path
from pathlib import Path
from yaml import FullLoader, load

DIR_PATH = str(Path(path.dirname(path.realpath(__file__))))

with open(DIR_PATH + "/version.yaml") as file:
    VERSION = load(file, Loader=FullLoader)

ABOUT = {
    "name": "flask-app",
    **VERSION,
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
            "werkzeug",
        ],
        "databases": [
            "sqlite",
            "mysql",
            "postgres",
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
