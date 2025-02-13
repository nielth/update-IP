FROM python:alpine AS post-info

WORKDIR /app

COPY main.py .
COPY requirements.txt .
COPY .env .

RUN pip3 install -r requirements.txt

CMD [ "python", "-u", "main.py" ]
