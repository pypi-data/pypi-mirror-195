"""Image info"""

from PIL import Image
from PIL.ExifTags import TAGS

def meta(src: str) -> dict:
    """Meta of image"""
    image = Image.open(src)
    return {"height": image.height, "width": image.width, "format": image.format, "mode": image.mode, "animated": getattr(image, "is_animated", False), "frames": getattr(image, "n_frames", 1)}

def exif(src: str) -> dict:
    """Exif of image"""
    image = Image.open(src)
    exifdata = image.getexif()
    result = {}
    for tag_id in exifdata:
        tag = TAGS.get(tag_id, tag_id)
        data = exifdata.get(tag_id)
        if isinstance(data, bytes):
            data = data.decode()
        result[tag] = data
    return result
