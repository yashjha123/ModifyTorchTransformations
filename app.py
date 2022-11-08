import flask
from flask import request, jsonify
import os

import torch
import torchvision

import uuid
from flask_cors import CORS, cross_origin
import PIL
from PIL import Image
import json

UPLOAD_FOLDER ="./folder/"

app = flask.Flask(__name__)
CORS(app)
val123 = [] #TODO IMPLEMENT DATABASE FOR THIS
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
import io

class JsonDatabase():
    def __init__(self,initialState=[]):
        super().__init__()
        self.state = initialState
        self.loadState()
    def saveState(self):
        print(self.state)
        with open('data.json', 'w') as f:
            json.dump(self.state, f)
    def loadState(self):
        with open('data.json','r') as f:
            self.state = json.load(f)
    def add(self,val):
        self.loadState()
        updateState = ({**val,"id":uuid.uuid4().hex})
        self.state.append(updateState)
        self.saveState()
        return updateState
    def lookFor(self,id):
        self.loadState()
        for val in self.state:
            print(val)
            if val["id"]==id:
                return val
        return False
database = JsonDatabase()
@app.route('/fileUpload', methods=["POST"])
@cross_origin()
def get_id():
    # if 'image' not in rzequest.files:
    # #     return "<p>No file!</p>"
    print(request.files)
    file1 = request.files['file']
    path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
    file1.save(path)
    val = database.add({"path":path})
    print((val))
    return jsonify(val)
# import PIL
# @app.route('/getImage'):
#     return flask.send_file(
#         output,
#         mimetype='image/png',
#         as_attachment=True,
#         download_name='%s.png' % file_path["id"])

@app.route('/applyTransformations', methods=["POST"])
@cross_origin()
def applyTransformations():
    print(request.is_json)
    obj = request.json
    # print(request.form[''])
    print()
    file_path = database.lookFor(obj["id"])
    img = Image.open(file_path["path"])
    print(obj["transforms"])
    tts = []
    exec("tts.append("+obj["transforms"]+")",{},{"tts":tts,"transforms":torchvision.transforms,'torchvision':torchvision,'torch':torch})
    img = tts[0](img)
#     imgFilePath = 
    print(type(img)==PIL.PngImagePlugin.PngImageFile)
    # img = torchvision.transforms.ToPILImage()(img)
    # print(img)
    # flask.make_response
    global val123
    val123 = io.BytesIO()
    img.save(val123, format='PNG')
    # img.save("img.png")
    # print(val123.getvalue())
    response = flask.make_response(val123.getvalue())
    response.headers.set('Content-Type', 'image/png')
    response.headers.set(
        'Content-Disposition', 'attachment', filename='%s.png' % file_path["id"])
    return response
    # print(val123)
    # return jsonify({"database":request.json["id"],'val':str(type(img))})
    # return flask.send_file(
    #     val123,
    #     mimetype='image/png',
    #     as_attachment=True,
    #     download_name='%s.png' % file_path["id"])
@app.route('/', methods=['GET', 'POST'])
def home():
    return flask.render_template('./filename.html')


if __name__ == '__main__':
    app.run()