from python:3.6-stretch

expose 80/tcp

workdir /app

copy . /app

run pip3 install -r requirement.txt

cmd ["python", "app.py"]