FROM python:3.9-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN sed -i 's/http:\/\/[a-zA-Z0-9]*.[a-zA-Z0-9]*.*.com/http:\/\/ir.ubuntu.sindad.cloud/g' /etc/apt/sources.list

COPY requirements.txt /app/

RUN python -m pip install --upgrade pip -i https://mirror-pypi.runflare.com/simple
RUN pip install -r requirements.txt -i https://mirror-pypi.runflare.com/simple

COPY ./core /app

CMD ["python3","manage.py","runserver","0.0.0.0:8000"]