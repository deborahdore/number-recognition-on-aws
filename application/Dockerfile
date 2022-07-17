FROM python:3 AS py3
FROM openjdk:8

COPY --from=py3 / /

COPY . .
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install -r requirements.txt

ENV S3_BUCKET_NAME "number-recognition-bucket-v1"
ENV ACCESS_KEY "xx"
ENV SECRET_KEY "xxx"

HEALTHCHECK  --interval=300s \
    CMD wget --no-verbose --tries=5 --spider http://localhost:5000 || exit 1

ENTRYPOINT ["python", "app.py"]