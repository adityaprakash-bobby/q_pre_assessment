FROM alpine:3.7

WORKDIR app/

COPY requirements.txt .

COPY app.py .

RUN apk add --update \
    python \
    python-dev \
    py-pip \
    build-base

RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["python", "app.py"]
