FROM python:3.8

WORKDIR /app

COPY requirements.txt .

RUN pip install  --no-cache-dir -r requirements.txt

COPY nameko.yml nameko.yml
COPY src src/.

CMD [ "nameko", "run", "--config", "./nameko.yml", "src.service"]