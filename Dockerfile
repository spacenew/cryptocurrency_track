FROM python:3.9.9-slim

RUN pip install -U pip
RUN pip install pipenv

WORKDIR /app

RUN pipenv install --system --deploy

COPY . /app

EXPOSE 9696

ENTRYPOINT [ "gunicorn", "--bind=0.0.0.0:9696", "predict:app" ]