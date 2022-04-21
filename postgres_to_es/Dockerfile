FROM python:3.10-slim-buster
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt --no-cache-dir
CMD ["python", "etl.py"]

