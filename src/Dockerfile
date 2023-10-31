FROM python:3.11

LABEL author="Rodrigo Lopes"
LABEL github="github.com/rodzera"

COPY . /src

RUN apt update ; apt upgrade -y ; apt install vim -y ;  apt clean

RUN pip install -U pip ; pip install -r /src/requirements.txt

RUN chmod +x /src/entrypoint.sh

ENTRYPOINT ["/src/entrypoint.sh"]