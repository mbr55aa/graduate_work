FROM python:3.10-slim-buster

EXPOSE 8001

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY ./requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8001"]