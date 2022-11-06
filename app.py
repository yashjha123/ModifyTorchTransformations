import flask
from flask import request
import os
UPLOAD_FOLDER ="./folder/"

app = flask.Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/fileUpload', methods=["POST"])
def get_id():
    if 'image' not in request.files:
        return "<p>No file!</p>"
    file1 = request.files['image']
    path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
    file1.save(path)
    return path

@app.route('/', methods=['GET', 'POST'])
def home():
    return flask.render_template('./filename.html')


if __name__ == '__main__':
    app.run()