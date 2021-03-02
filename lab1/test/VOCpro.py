from random import shuffle
from tqdm import tqdm
import cv2
import os

base = 'VOCData'

imgs = [v for v in os.listdir(base) if v.endswith('.jpg')]

shuffle(imgs)

with open('train.txt', 'w') as f:
  for im in tqdm(imgs):
    xml = im[:-4]+'.xml'
    info = im + ' ' + xml
    if not cv2.imread(os.path.join(base, im)) is None:
      f.write(info+'\n')

with open('eval.txt', 'w') as f:
  for im in tqdm(imgs):
    xml = im[:-4]+'.xml'
    info = im + ' ' + xml
    if not cv2.imread(os.path.join(base, im)) is None:
      f.write(info+'\n')

labels = ['black', 'white']
with open('labels.txt', 'w') as f:
  for lbl in labels:
    f.write(lbl+'\n')