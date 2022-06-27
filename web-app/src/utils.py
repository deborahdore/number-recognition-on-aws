import cv2
import numpy as np
import pandas as pd
from PIL import Image
from pyspark.sql.types import StructField, IntegerType, StructType

from src.conf import COLUMNS


def crop_image(img):
    # TODO
    pass


def resize_image(img):
    return cv2.resize(img, (28, 28))


def to_BW(img):
    gray = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
    (thresh, blackAndWhiteImage) = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    # cv2.imwrite("photo.jpg", blackAndWhiteImage)
    return blackAndWhiteImage


def img_transform(img):
    raw = np.array(Image.open(img))
    # TODO
    # crop = crop_image(raw)
    # also number must be white and background black - invert colors if not the case
    resize = resize_image(raw)
    gray = to_BW(resize)
    return np.array(gray, dtype=np.int32).flatten()


def to_dataframe(array, spark):
    pd_df = pd.DataFrame([array], columns=COLUMNS).astype('int32')

    fields = [StructField(field_name, IntegerType(), False) for field_name in COLUMNS]

    spark_df = spark.createDataFrame(pd_df, schema=StructType(fields))
    spark_df.show()
    return spark_df
