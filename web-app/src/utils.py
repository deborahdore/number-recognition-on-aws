import cv2
import numpy as np
import pandas as pd
from PIL import Image
from pyspark.sql.types import StructField, IntegerType, StructType

from src.conf import COLUMNS


def crop_image(img):
    h, w = img.shape
    if w > h:
        rm = int((w - h) / 2)
        cropped = img[:, rm:w - rm]

    else:
        rm = int((h - w) / 2)
        cropped = img[rm: h - rm, :]

    # cv2.imwrite("cropped.png", cropped)
    return cropped


def resize_image(img):
    resize = cv2.resize(img, (28, 28))
    # cv2.imwrite("resize.png", resize)
    return resize


def to_BW(img):
    gray = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
    (thresh, b_and_w_image) = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    # invert colors if number is not white
    # count white
    count_b = np.count_nonzero(b_and_w_image == 0)
    count_w = np.count_nonzero(b_and_w_image == 255)

    if count_w > count_b:
        b_and_w_image = cv2.bitwise_not(b_and_w_image)

    # cv2.imwrite("photo.jpg", b_and_w_image)

    return b_and_w_image


def img_transform(img):
    raw = np.array(Image.open(img))
    gray = to_BW(raw)
    # crop = crop_image(gray)
    resize = resize_image(gray)
    return np.array(resize, dtype=np.int32).flatten()


def to_dataframe(array, spark):
    pd_df = pd.DataFrame([array], columns=COLUMNS).astype('int32')

    fields = [StructField(field_name, IntegerType(), False) for field_name in COLUMNS]

    spark_df = spark.createDataFrame(pd_df, schema=StructType(fields))
    spark_df.show()
    return spark_df
