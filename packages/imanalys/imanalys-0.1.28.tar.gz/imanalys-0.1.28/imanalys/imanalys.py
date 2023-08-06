
from dataclasses import dataclass
from typing import List, Optional
import json
from imanalys import file, image, text, person, nsfw

@dataclass
class Model:

    name: Optional[str] = None
    size: Optional[int] = None
    url: Optional[str] = None
    path: Optional[str] = None
    meta: Optional[dict] = None
    exif: Optional[dict] = None
    text: Optional[dict] = None
    person: Optional[dict] = None
    nsfw: Optional[dict] = None

class SetModel:

    def __init__(self, source: dict):
        self._source = source

    def as_model(self) -> Model:
        model = Model()
        model.name = self._source.get("name")
        model.size = self._source.get("size")
        model.url = self._source.get("url")
        model.path = self._source.get("path")
        model.meta = self._source.get("meta")
        model.exif = self._source.get("exif")
        model.text = self._source.get("text")
        model.person = self._source.get("person")
        model.nsfw = self._source.get("nsfw")
        return model

    def as_json(self) -> json:
        return json.dumps(self.as_model().__dict__)

def get(url=None, path=None, temp='/tmp', output=None) -> Optional[Model]:
    params = {}
    if url is None and path is not None:
        params['path'] = path
        file_path = file.move(src=params['path'], temp=temp)
    if url is not None and path is None:
        params['url'] = url
        file_path = file.download(url=params['url'], temp=temp)
    params['name'] = file.name(file_path)
    params['size'] = file.size(file_path)
    params['meta'] = image.meta(file_path)
    params['exif'] = image.exif(file_path)
    params['text'] = text.get(file_path)
    params['person'] = person.get(file_path)
    params['nsfw'] = nsfw.get(file_path)

    file.delete(file_path)
    if output is None:
        return SetModel(params).as_json()
    return SetModel(params).as_model()
