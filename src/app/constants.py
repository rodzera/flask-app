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
            "flask-sqlalchemy",
            "flask-migrate",
            "flask-marshmallow",
            "flasgger",
            "gunicorn",
            "werkzeug",
        ],
        "databases": [
            "postgres",
            "mysql"
        ],
        "tests": [
            "pytest"
        ],
        "ci/cd": [
            "github actions"
        ],
        "devops": [
            "docker"
        ]
    }
}
