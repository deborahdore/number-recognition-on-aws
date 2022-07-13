FROM python:3 AS py3
FROM openjdk:8

COPY --from=py3 / /

COPY . .
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install -r requirements.txt

ENV S3_BUCKET_NAME "number-recognition-on-aws-bucket"
ENV ACCESS_KEY "AKIAUGHEIUPRAYAK2IRR"
ENV SECRET_KEY "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"

ENTRYPOINT ["python", "app.py"]