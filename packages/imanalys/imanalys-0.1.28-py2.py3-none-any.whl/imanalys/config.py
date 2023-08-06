import os

nsfw = {
    "model": os.path.join(os.path.dirname(__file__), "data/nsfw_mobilenet2.224x224.h5")
}

person = {
    "face_proto": os.path.join(os.path.dirname(__file__), "data/opencv_face_detector.pbtxt"),
    "face_model": os.path.join(os.path.dirname(__file__), "data/opencv_face_detector_uint8.pb"),
    "age_proto": os.path.join(os.path.dirname(__file__), "data/age_deploy.prototxt"),
    "age_model": os.path.join(os.path.dirname(__file__), "data/age_net.caffemodel"),
    "gender_proto": os.path.join(os.path.dirname(__file__), "data/gender_deploy.prototxt"),
    "gender_model": os.path.join(os.path.dirname(__file__), "data/gender_net.caffemodel"),
    "model_values": (78.4263377603, 87.7689143744, 114.895847746),
    "age_list": ["0-2", "4-6", "8-12", "15-20", "25-32", "38-43", "48-53", "60-100"],
    "gender_list": ["Male", "Female"],
    "conf_threshold": 0.3,
    "width": 760,
    "padding" : 1,
}

text = {
    "languages": "eng+deu+rus+fra",
    "config": r"--oem 3 --psm 6",
}
