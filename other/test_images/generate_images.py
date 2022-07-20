from PIL import Image

size = 28
increase = 70
n_images = 100
img = Image.open('images/img28.png')
for i in range(n_images):
    size = size + increase
    resized_img = img.resize((size, size))
    resized_img.save('images/img{}.png'.format(size))
