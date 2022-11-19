import io
import flask
from flask import request, jsonify
import os

from requests_toolbelt import MultipartEncoder

from flask import send_from_directory


import numpy as np
import torch
import torchvision

import base64
import cv2
import uuid
from flask_cors import CORS, cross_origin
import PIL
from PIL import Image
import json

import utils
UPLOAD_FOLDER = "./folder/"

app = flask.Flask(__name__)
CORS(app)
val123 = []  # TODO IMPLEMENT DATABASE FOR THIS
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


class JsonDatabase():
    def __init__(self, initialState=[]):
        super().__init__()
        self.state = initialState
        self.loadState()

    def saveState(self):
        with open('data.json', 'w') as f:
            json.dump(self.state, f)

    def loadState(self):
        with open('data.json', 'r') as f:
            self.state = json.load(f)

    def add(self, val):
        self.loadState()
        updateState = ({**val, "id": uuid.uuid4().hex})
        self.state.append(updateState)
        self.saveState()
        return updateState

    def lookFor(self, id):
        self.loadState()
        for val in self.state:
            if val["id"] == id:
                return val
        return False


database = JsonDatabase()

@app.route('/file/<path:path>')
def get_file(path):
    return send_from_directory('folder/imgs', path)

@app.route('/fileUpload', methods=["POST"])
@cross_origin()
def get_id():
    # if 'image' not in rzequest.files:
    # #     return "<p>No file!</p>"

    file1 = request.files['file']
    path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
    file1.save(path)
    val = database.add({"path": path})
    
    return jsonify(val)


def error(msg, e):
    return ({"message": msg, "error": str(e)}), 500


@app.route('/applyTransformations', methods=["POST"])
@cross_origin()
def applyTransformations():
    print(request.is_json)
    obj = request.json
    conf = obj["conf"]
    # print(request.form[''])
    print(conf)
    file_path = database.lookFor(obj["id"])
    img = Image.open(file_path["path"]).convert('RGB')
    # img = torchvision.io.read_image(file_path["path"])
    # print(img.shape)
    # return
    print(obj["transforms"])
    custom = []
    try:
        exec("tts.append("+obj["transforms"]+")", {}, {"tts": custom,
             'torchvision': torchvision, "transforms": torchvision.transforms, 'torch': torch})
    except Exception as e:
        return error("Transformations not defined correctly! Error while processing transformations!", e)
    try:
        img = custom[0](img)
    except Exception as e:
        return error("Error occured while applying transformation!", e)
    file_type = ""

    buffer = io.BytesIO()
    is_scaled, is_normalised = False,False
    print(conf["scale_range"])
    if type(img) == torch.Tensor:
        file_type = "Tensor"

        if conf["scale_range"]:
            img, is_scaled = utils.scale_range(img)
        if conf["normalize_range"]:
            img, is_normalised = utils.normalize_range(img)

        img = img.numpy().astype(np.uint8)
        img = np.moveaxis(img, 0, -1)
        img = Image.fromarray(img)
        img.save(buffer, format='PNG')
    elif type(img) == np.ndarray:
        file_type = "Numpy"

        if conf["scale_range"]:
            img, is_scaled = utils.scale_range(img)
        if conf["normalize_range"]:
            img, is_normalised = utils.normalize_range(img)

        img = Image.fromarray(img)
        img.save(buffer, format='PNG')
    else:
        file_type = "PIL Image"
        img.save(buffer, format='PNG')
    print(conf["scale_range"])
    
    json_reponse = {"file_type": file_type,
                    "file_type_encoded": str(type(img)),
                    "is_scaled": is_scaled,
                    "is_normalised": is_normalised}
    # response = flask.make_response(buffer.getvalue())
    # response.headers.set('Content-Type', 'image/png')
    # response.headers.set('file_type',file_type)
    # response.headers.set('file_type_encoded',str(type(img)))
    # response.headers.set('is_scaled',is_scaled)
    # response.headers.set('is_scaled',is_normalised)
    # response.headers.set(
    #     'Content-Disposition', 'attachment', filename='%s.png' % file_path["id"])
    # return response
    m = MultipartEncoder(
        fields={
            'field0': (None, json.dumps(json_reponse), "application/json"),
            'field1': ("image.png", buffer, "image/png")
        }
    )
    return flask.Response(m.to_string(), mimetype=m.content_type)
    # return jsonify(json_reponse)


@app.route('/', methods=['GET', 'POST'])
def home():
    return flask.render_template('./filename.html')


if __name__ == '__main__':
    app.run()
