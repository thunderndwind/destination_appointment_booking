FROM python:3.12.2-slim-bullseye

WORKDIR /app

COPY requirements.txt .

RUN pip install --default-timeout=100 -r requirements.txt

COPY . .

EXPOSE 5000

CMD [ "python", "run.py"]