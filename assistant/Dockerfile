FROM python:3.10-slim-buster

EXPOSE 8001

WORKDIR /code

COPY ./requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir

CMD ["python", "app.py"]