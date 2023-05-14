FROM python:3.10-slim

RUN mkdir /app

RUN pwd

RUN ls

COPY ./requirements.txt app/

RUN pip3 install -r requirements.txt --no-cache-dir

COPY ./ /app

WORKDIR /app

CMD ["gunicorn", "backend.wsgi:application", "--bind", "0:8000"]