import argparse as ap
import cv2
import numpy as np
import os
from sklearn.externals import joblib
from scipy.cluster.vq import *

from sklearn import preprocessing
from rootsift import RootSIFT
import math


TRAIN_PATH = "path/to/training/dataset"
NUM_WORDS = 1000

training_names = os.listdir(TRAIN_PATH)

# Get all the path to the images and save them in a list
# image_paths and the corresponding label in image_paths
image_paths = []
for training_name in training_names:
    image_path = os.path.join(TRAIN_PATH, training_name)
    image_paths += [image_path]

# Create feature extraction and keypoint detector objects
feature_detector = cv2.FeatureDetector_create("SIFT")
descriptor_extractor = cv2.DescriptorExtractor_create("SIFT")

# List where all the descriptors are stored
des_list = []

for i, image_path in enumerate(image_paths):
    img = cv2.imread(image_path)
    print("Extract SIFT of %s image, %d of %d images" % (training_names[i], i, len(image_paths)))
    kpts = feature_detector.detect(img)
    kpts, des = descriptor_extractor.compute(img, kpts)
    # rootsift
    # rs = RootSIFT()
    # des = rs.compute(kpts, des)
    des_list.append((image_path, des))

# Stack all the descriptors vertically in a numpy array
# downsampling = 1
# descriptors = des_list[0][1][::downsampling,:]
# for image_path, descriptor in des_list[1:]:
#    descriptors = np.vstack((descriptors, descriptor[::downsampling,:]))

# Stack all the descriptors vertically in a numpy array
descriptors = des_list[0][1]
for image_path, descriptor in des_list[1:]:
    descriptors = np.vstack((descriptors, descriptor))

# Perform k-means clustering
print
"Start k-means: %d words, %d key points" % (NUM_WORDS, descriptors.shape[0])
voc, variance = kmeans(descriptors, NUM_WORDS, 1)

# Calculate the histogram of features
im_features = np.zeros((len(image_paths), NUM_WORDS), "float32")
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

joblib.dump((im_features, image_paths, idf, NUM_WORDS, voc), "bof.pkl", compress=3)
