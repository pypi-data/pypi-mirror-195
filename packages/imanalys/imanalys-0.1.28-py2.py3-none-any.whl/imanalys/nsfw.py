"""Recognisation of NSFW"""

from nsfw_detector import predict
import imanalys.config as cfg

MODEL_NSFW = cfg.nsfw['model']

def get(path: str) -> list:
    model = predict.load_model(MODEL_NSFW)
    result = predict.classify(model, path)
    if result:
        return result[path]
    return []
