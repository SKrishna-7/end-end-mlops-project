
FROM python:3.10-slim-buster

WORKDIR /app


COPY requirements.txt /app/


RUN pip install -r requirements.txt


COPY . /app


EXPOSE 5000


CMD ["python3", "app.py"]
