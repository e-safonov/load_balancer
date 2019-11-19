FROM python:3-alpine as base

FROM base as builder
RUN mkdir /install
RUN apk update && apk add gcc python3-dev musl-dev libc-dev linux-headers make
WORKDIR /install

COPY requirements.txt /requirements.txt

RUN pip install --install-option="--prefix=/install" -r /requirements.txt

FROM base
COPY --from=builder /install /usr/local
COPY . /usr/src/app/

WORKDIR /usr/src/app/
EXPOSE 9999
CMD ["python", "app.py"]
