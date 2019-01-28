from django.conf import settings
import cv2 as cv
import numpy as np
import os
from sklearn.externals import joblib
from scipy.cluster.vq import *
from sklearn import preprocessing
import requests


URL = 'http://127.0.0.1:8000/api/images/'
NUM_WORDS = 1000


def findFeatures(images):
    pass