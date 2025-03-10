FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 5000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

