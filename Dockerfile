FROM python:3-alpine

WORKDIR /user/src/app

COPY requirements.txt ./
RUN apk add --no-cache --virtual .build-deps gcc libc-dev linux-headers; pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["python", "./main.py"]