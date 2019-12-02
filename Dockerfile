FROM python:alpine3.6

RUN apk add --no-cache --update \
    python3 python3-dev gcc bash \
    gfortran musl-dev g++ \
    libffi-dev openssl-dev \
    libxml2 libxml2-dev \
    libxslt libxslt-dev \
    libjpeg-turbo-dev zlib-dev
RUN pip install --upgrade pip


WORKDIR /usr/src/app

EXPOSE 8000

RUN pip install -U pip \
                   gunicorn

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt	

COPY . .

CMD ["gunicorn", "--workers=2", "--bind=0.0.0.0:8000", "app:app"]
