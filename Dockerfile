FROM python:2.7-slim

WORKDIR /app

COPY boardgames /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

CMD ["python", "app.py"]