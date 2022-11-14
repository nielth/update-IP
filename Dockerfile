FROM python:alpine AS post-info

WORKDIR /app

COPY main.py .
COPY requirements.txt .
COPY crontab .
COPY .env .

RUN pip3 install -r requirements.txt

RUN crontab crontab 

CMD ["crond", "-f"]
# CMD [ "python3", "main.py" ]