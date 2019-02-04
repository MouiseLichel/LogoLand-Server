import cv2
from pylab import *
from rest_framework.settings import settings
from scipy.cluster.vq import *
from sklearn import preprocessing
from sklearn.externals import joblib

DICTIONARY = settings.DICTIONARY_PATH


# Get query image path
def search(opencv_image):
    # Load the classifier, class names, scaler, number of clusters and vocabulary
    im_features, image_paths, idf, numWords, voc = joblib.load(DICTIONARY)

    # Create feature extraction and keypoint detector objects
    # List where all the descriptors are stored
    des_list = []
    sift = cv2.xfeatures2d.SIFT_create()

    gray = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)
    kp, des = sift.detectAndCompute(opencv_image, None)

    des_list.append(("image_path", des))

    # Stack all the descriptors vertically in a numpy array
    descriptors = des_list[0][1]

    #
    test_features = np.zeros((1, numWords), "float32")
    words, distance = vq(descriptors, voc)
    for w in words:
        test_features[0][w] += 1

    # Perform Tf-Idf vectorization and L2 normalization
    test_features = test_features * idf
    test_features = preprocessing.normalize(test_features, norm='l2')

    score = np.dot(test_features, im_features.T)
    rank_ID = np.argsort(-score)

    image_urls = [settings.MEDIA_URL + image_name for image_name in image_paths]

    results = []

    for i, ID in enumerate(rank_ID[0][0:16]):
        print("img_name:%s, score:%s"%(image_paths[ID],score[0][ID]))
        results.append({'image_url': image_urls[ID], 'score': score[0][ID]})

    return results