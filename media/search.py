import json
class Result(object):
    def __init__(self, image_url,score):
        self.image_url = image_url
        self.score = score

def search(image):
    results =[]
    result1 = Result('127.0.0.1/media/ukbench00000.jpg', 0.92)
    result2 = Result('127.0.0.1/media/ukbench00001.jpg', 0.84)
    results.append(result1.__dict__)
    results.append(result2.__dict__)
    return json.dumps(results)