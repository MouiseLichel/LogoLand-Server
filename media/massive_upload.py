import argparse as ap
import os
from io import BytesIO
from PIL import Image as ImagePillow
import requests
import base64
import json
from findFeatures import findFeatures
import numpy

URL = 'http://127.0.0.1:8000/api/images/'
DEFAULT_TRAINING_SET_PATH = 'C:/Users/L0u15/Documents/imt/inged2/image-mobile/image-retrieval/bag-of-words-python-dev-version/dataset/train'


def deleteAllImages():
    # Get all image ids
    ids = []
    r = requests.get(URL)
    if r.status_code != 200:
        print(r.status_code)
        print(r.json)
        exit()
    ids = [image['pk'] for image in r.json()]

    # Delete all images
    for id in ids:
        r = requests.delete(URL + str(id))
        if r.status_code != 204:
            print(r.status_code)
            print(r.json)
            exit()
        print("Image %s deleted" % id)


def uploadImages(image_paths):
    for image_path in image_paths:
        image_file = open(image_path, 'rb')
        payload = {'image': image_file}
        r = requests.post(URL, files=payload)
        if r.status_code == 201:
            old_name = os.path.basename(image_path)
            data = r.json()
            new_name = os.path.basename(data['image'])
            print("Image '%s' upload under the name of '%s'" % (old_name, new_name))
        else:
            print(r.status_code)
            print(r.json)


def getImagePaths(dataset_path):
    training_names = os.listdir(train_path)
    # Get all the path to the images and save them in a list
    # image_paths and the corresponding label in image_paths
    image_paths = []
    for training_name in training_names:
        image_path = os.path.join(train_path, training_name)
        image_paths.append(image_path)

    return image_paths


def getImageURLs():
    r = requests.get(URL)
    if r.status_code == 200:
        urls = [image['image'] for image in r.json()]
    return urls


def getMapImageUrl(image_urls):
    map = {}
    for image_url in image_urls:
        r = requests.get(image_url)
        opencv_image = numpy.array(ImagePillow.open(BytesIO(r.content)))
        map[image_url] = opencv_image
    return map


if __name__ == "__main__":
    # Get the path of the training set
    parser = ap.ArgumentParser()
    parser.add_argument("-t", "--trainingSet", help="Path to Training Set",
                        required=True)
    args = vars(parser.parse_args())

    # Get image paths
    train_path = args["trainingSet"]
    image_paths = getImagePaths(train_path)

    # Delete and Upload all images
    # deleteAllImages()
    # uploadImages(image_paths)
    image_urls = getImageURLs()
    images = getMapImageUrl(image_urls)
    findFeatures(images)
