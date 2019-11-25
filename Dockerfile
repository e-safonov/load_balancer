FROM python:3-alpine

RUN apk update && apk add gcc python3-dev musl-dev libc-dev linux-headers make
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
COPY . /usr/src/app/
WORKDIR /usr/src/app/
EXPOSE 9999

COPY ./entry_point.sh /
RUN chmod +x /entry_point.sh
ENTRYPOINT ["/entry_point.sh"]
