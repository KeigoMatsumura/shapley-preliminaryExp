import os
from PIL import Image
import imagehash

userpath = './masked-img'  # 検索するパス

image_files = []
f = [os.path.join(userpath, path) for path in os.listdir(userpath)]
for i in f:
    if i.endswith('.jpg') or i.endswith('.png'):
        image_files.append(i)

imgs = {}
for img in sorted(image_files):
    hash = imagehash.average_hash(Image.open(img))
    if hash in imgs:
        print('Similar image :', img, imgs[hash])
    else:
        imgs[hash] = img