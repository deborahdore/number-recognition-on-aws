import math
import os

import pandas as pd

import immagini

folder = './images'
image_number = 12000
df = pd.read_csv('mnist_train.csv')
df.drop('label', axis=1, inplace=True)
dim = int(math.sqrt((df.shape[1])))

for i, entry in df.iterrows():
    img = []
    for j in range(dim):
        row = []
        for k in range(dim):
            c = entry[dim * j + k]
            row.append((c, c, c))
        img.append(row.copy())
    immagini.save(img, os.path.join(folder, 'img{}.png').format(i))
    if i == image_number - 1:
        break
