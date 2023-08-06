"""Recognisation of persons"""

import cv2
from PIL import Image
import imanalys.config as cfg

FACE_PROTO = cfg.person['face_proto']
FACE_MODEL = cfg.person['face_model']
AGE_PROTO = cfg.person['age_proto']
AGE_MODEL = cfg.person['age_model']
GENDER_PROTO = cfg.person['gender_proto']
GENDER_MODEL = cfg.person['gender_model']
MODEL_MEAN_VALUES = cfg.person['model_values']
AGE_LIST = cfg.person['age_list']
GENDER_LIST = cfg.person['gender_list']
TRESHOLD = cfg.person['conf_threshold']
WIDTH = cfg.person['width']
PADDING = cfg.person['padding']

def get(path: str) -> list:
    if not hasattr(Image, 'Resampling'):  # Pillow<9.0
        Image.Resampling = Image
    result = ''
    FACE_NET = cv2.dnn.readNet(FACE_MODEL, FACE_PROTO)
    AGE_NET = cv2.dnn.readNet(AGE_MODEL, AGE_PROTO)
    GENDER_NET = cv2.dnn.readNet(GENDER_MODEL, GENDER_PROTO)
    img = Image.open(path)
    iw = img.size[0]
    ih = img.size[1]
    wpercent = (WIDTH/float(iw))
    hsize = int((float(ih)*float(wpercent)))
    img = img.resize((WIDTH,hsize), Image.Resampling.LANCZOS)
    img.save(path)
    image = cv2.imread(path)
    frame = image.copy()
    frame_face = frame.copy()
    frame_height = frame_face.shape[0]
    frame_width = frame_face.shape[1]
    blob = cv2.dnn.blobFromImage(frame_face, 1.0, (300, 300), [104, 117, 123], True, False)
    FACE_NET.setInput(blob)
    detections = FACE_NET.forward()
    boxes = []
    condidates = range(detections.shape[2])
    for i in condidates:
        confidence = detections[0, 0, i, 2]
        if confidence > TRESHOLD:
            x1 = int(detections[0, 0, i, 3] * frame_width)
            y1 = int(detections[0, 0, i, 4] * frame_height)
            x2 = int(detections[0, 0, i, 5] * frame_width)
            y2 = int(detections[0, 0, i, 6] * frame_height)
            boxes.append([x1, y1, x2, y2])
            # cv2.rectangle(frame_face, (x1, y1), (x2, y2), (0, 255, 0), int(round(frame_height / 150)), 8)
            cv2.rectangle(frame_face, (x1, y1), (x2, y2), (0, 255, 0), 2, 8)
    data = []
    total = len(boxes)
    for box in boxes:
        face = frame[max(0, box[1] - PADDING):min(box[3] + PADDING, frame.shape[0] - 1), max(0, box[0] - PADDING):min(box[2] + PADDING, frame.shape[1] - 1)]
        blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB = False)
        GENDER_NET.setInput(blob)
        gender_predictions = GENDER_NET.forward()
        gender = GENDER_LIST[gender_predictions[0].argmax()]
        # print("Gender: {}, conf: {:.3f}".format(gender, gender_predictions[0].max()))
        AGE_NET.setInput(blob)
        age_predictions = AGE_NET.forward()
        age = AGE_LIST[age_predictions[0].argmax()]
        # print("Age: {}, conf: {:.3f}".format(age, age_predictions[0].max()))
        data.append({'gender': gender, 'age': age})
    return data
