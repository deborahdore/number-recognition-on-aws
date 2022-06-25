FROM python:3 AS py3
FROM openjdk:8

COPY --from=py3 / /

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]

CMD ["app.py"]