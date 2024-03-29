import os
import argparse as ap
import cv2
import numpy as np
from rest_framework.settings import settings
from scipy.cluster.vq import *
from sklearn import preprocessing
from sklearn.externals import joblib
from django.core import exceptions

# Get training dataset path and dictionary
try:
    train_path = settings.TRAIN_PATH
    dictionary = settings.DICTIONARY_PATH
except exceptions.ImproperlyConfigured:
    parser = ap.ArgumentParser()
    parser.add_argument("-t", "--trainingSet", help="Path to Training Set", required="True")
    parser.add_argument("-d", "--dictionary", help="Path to Dictionary", required="True")
    args = vars(parser.parse_args())

    # Get the training classes names and store them in a list
    train_path = args["trainingSet"]
    dictionary = args["dictionary"]

training_names = os.listdir(train_path)

numWords = 1000

# Get all the path to the images and save them in a list
# image_paths and the corresponding label in image_paths
image_paths = []
for training_name in training_names:
    image_path = os.path.join(train_path, training_name)
    image_paths += [image_path]

# List where all the descriptors are stored
des_list = []
sift = cv2.xfeatures2d.SIFT_create()

for i, image_path in enumerate(image_paths):
    im = cv2.imread(image_path)
    print("Extract SIFT of %s image, %d of %d images" % (training_names[i], i, len(image_paths)))
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    kp, des = sift.detectAndCompute(gray, None)
    des_list.append((image_path, des))

# Stack all the descriptors vertically in a numpy array
descriptors = des_list[0][1]
for image_path, descriptor in des_list[1:]:
    descriptors = np.vstack((descriptors, descriptor))

# Perform k-means clustering
print("Start k-means: %d words, %d key points" % (numWords, descriptors.shape[0]))
voc, variance = kmeans(descriptors, numWords, 1)

# Calculate the histogram of features
im_features = np.zeros((len(image_paths), numWords), "float32")
for i in range(len(image_paths)):
    words, distance = vq(des_list[i][1], voc)
    for w in words:
        im_features[i][w] += 1

# Perform Tf-Idf vectorization
nbr_occurences = np.sum((im_features > 0) * 1, axis=0)
idf = np.array(np.log((1.0 * len(image_paths) + 1) / (1.0 * nbr_occurences + 1)), 'float32')

# Perform L2 normalization
im_features = im_features * idf
im_features = preprocessing.normalize(im_features, norm='l2')

joblib.dump((im_features, training_names, idf, numWords, voc), dictionary, compress=3)
