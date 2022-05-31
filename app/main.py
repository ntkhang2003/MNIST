from flask import Flask, request, jsonify, render_template

from torch_utils import transform_image, get_prediction

app = Flask(__name__,template_folder='templates')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
def allowed_file(filename):
    # xxx.png
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def load():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def predict():
    imagefile = request.files['imagefile']
    image_path = "./assets/" + imagefile.filename
    imagefile.save(image_path)

    if imagefile is None or imagefile.filename == "":
        return render_template('index.html', error='no file')
    if not allowed_file(imagefile.filename):
        return render_template('index.html', error='format not supported')

    try:
        imagefile = open(image_path, 'rb')
        img_bytes = imagefile.read()
        tensor = transform_image(img_bytes)
        prediction = get_prediction(tensor)
        classification = str(prediction.item())
        return render_template('index.html', prediction=classification)
    except:
        return render_template('index.html', error='error during prediction')
if __name__ == '__main__':
    app.run(port = 3000, debug = True)