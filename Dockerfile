FROM python:3.9-slim

LABEL "devops.maintainers"="João Guedes <joao.guedes@grupoge21.com>, <joao.guedes@sga.pucminas.br>"

COPY . /app

COPY ./requirements.txt /app

WORKDIR /app

RUN pip3 install -r requirements.txt

EXPOSE 8000

CMD [ "uvicorn", "main:app", "--host=0.0.0.0", "--reload" ]