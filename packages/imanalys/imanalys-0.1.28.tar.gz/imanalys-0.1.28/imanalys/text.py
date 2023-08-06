"""Recognisation of text"""

import cv2
import pytesseract
from pytesseract import Output
import imanalys.config as cfg

TEXT_DETECTION_LANGUAGES = cfg.text['languages']
TEXT_CUSTOM_CONFIG = cfg.text['config']

def get(path: str) -> list:
    img = cv2.imread(path)
    height, width, channel = img.shape
    if width > 1000:
        img = cv2.resize(img, (width//2, height//2))
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh_img = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    ocr_output_details = pytesseract.image_to_data(thresh_img, output_type = Output.DICT, config=TEXT_CUSTOM_CONFIG, lang=TEXT_DETECTION_LANGUAGES)
    n_boxes = len(ocr_output_details['level'])
    for i in range(n_boxes):
        (x, y, w, h) = (ocr_output_details['left'][i], ocr_output_details['top'][i], ocr_output_details['width'][i], ocr_output_details['height'][i])
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    output_text = []
    word_list = []
    last_word = []
    for word in ocr_output_details['text']:
        if word != '':
            word_list.append(word)
            last_word = word
        if (last_word != '' and word == '') or (word == ocr_output_details['text'][-1]):
            if len(word_list) > 0:
                output_text.append(word_list)
            word_list = []
    return output_text
