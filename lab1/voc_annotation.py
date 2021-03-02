# -*- coding:utf-8 -*-
import xml.etree.ElementTree as ET
from os import getcwd

sets = ['train', 'val', 'test']
classes = ["black", "white"]


def convert_annotation(image_id, list_file):
    print(image_id)
    in_file = open('dataset/Annotations/%s.xml' % image_id)
    tree = ET.parse(in_file)
    root = tree.getroot()

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text), int(xmlbox.find('xmax').text), int(xmlbox.find('ymax').text))
        list_file.write(" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))

wd = getcwd()

for image_set in sets:
    image_ids = open('dataset/ImageSets/Main/%s.txt' % image_set).read().strip().split()
    print(image_ids)
    list_file = open('%s.txt' % image_set, 'w')

    for image_id in image_ids:
        list_file.write('dataset/JPEGImages/%s.jpg' % image_id)
        convert_annotation(image_id, list_file)
        list_file.write('\n')
    list_file.close()
