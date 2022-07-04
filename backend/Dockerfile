FROM python:3 AS py3
FROM openjdk:8

COPY --from=py3 / /

COPY . .

RUN pip install -r requirements.txt

ENV S3_BUCKET_NAME "cloud-project-adi-2"
ENV ACCESS_KEY "AKIAZU7SO2WVSUH44Y5X"
ENV SECRET_KEY "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"


ENTRYPOINT ["python"]

CMD ["main.py"]