import spacy
import os
import string
import cv2
import numpy as np

"""
Here the interpretation of user answers is happening (yes or no) 
with the use of previously trained model
Special  case for 'START' is used
"""

current_dir = os.getcwd()





def interpret_text_answer(message: str):
    nlp = spacy.load(os.path.join(current_dir, 'backCommands', 'interpretation_model', 'textmodel'))

    message = message.lower()

    translator = str.maketrans('', '', string.punctuation)

    message = message.translate(translator)

    if message == 'start' or message == '/start':
        return 'START'

    doc = nlp(message)

    if doc.cats['YES'] > 0.71:
        return "YES"

    if doc.cats['NO'] > 0.71:
        return "NO"

    return "UNKNOWN"


def interpret_image_answer(img):
    image_bytes = img.read()

    image_np = np.frombuffer(image_bytes, dtype=np.uint8)

    # Decode the numpy array as an image
    image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    path_to_classifier = os.path.join(current_dir, 'backCommands', 'interpretation_model', 'imagemodel', 'classifier.xml')

    cat_cascade = cv2.CascadeClassifier(path_to_classifier)

    cats = cat_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(cats) > 0:
        return 'YES'

    return 'UNKNOWN'