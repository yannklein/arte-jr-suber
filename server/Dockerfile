FROM python:3.10-slim-buster

WORKDIR /

COPY requirements.txt ./

RUN apt-get -y update 
RUN apt-get -y upgrade 
RUN apt-get install -y ffmpeg

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=/app.py

EXPOSE 8080

CMD [ "flask", "run", "--host=0.0.0.0", "--port=8080"]
