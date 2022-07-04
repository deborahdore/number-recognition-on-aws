import os

COLUMNS = ['pixel{:d}'.format(k) for k in range(784)]

S3_BUCKET_NAME = os.environ['S3_BUCKET_NAME']
ACCESS_KEY = os.environ['ACCESS_KEY']
SECRET_KEY = os.environ['SECRET_KEY']

BEST_MODEL_DIR = f's3a://{S3_BUCKET_NAME}/models'