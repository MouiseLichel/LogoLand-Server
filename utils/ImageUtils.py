import base64
from PIL import Image as PilImage
from io import BytesIO
import cv2
import numpy

def base64ToOpenCV(base64_image):
    decoded_string = base64.b64decode(str(base64_image))
    pil_image = PilImage.open(BytesIO(decoded_string))
    opencv_image = cv2.cvtColor(numpy.array(pil_image), cv2.COLOR_RGB2BGR)
    return opencv_image