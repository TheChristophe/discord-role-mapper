FROM python:3.12.7-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ADD ["config.py", "main.py", "role_mapper.py", "./"]

ENTRYPOINT ["python", "./main.py"]
