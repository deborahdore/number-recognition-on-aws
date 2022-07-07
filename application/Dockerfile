FROM python:3 AS py3
FROM openjdk:8

COPY --from=py3 / /

COPY . .
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install -r requirements.txt

ENV S3_BUCKET_NAME "number-recognition-on-aws-bucket"
ENV ACCESS_KEY "xx"
ENV SECRET_KEY "xxx"

ENTRYPOINT ["python", "app.py"]