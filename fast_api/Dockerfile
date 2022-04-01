FROM tiangolo/uvicorn-gunicorn:python3.9-slim

EXPOSE 8000

WORKDIR /fast_api

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir

COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
