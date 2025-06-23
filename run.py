from flask import Flask, render_template, request, redirect, url_for
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

model = load_model('SDSSmodel.h5')
labels = ['Cigar-shaped smooth', 'In between smooth', 'completely round smooth', 'edge-on', 'spiral']

def preprocess_image(image_path):
    img = load_img(image_path, target_size=(256, 256))  # matches model's expected input
    img_array = img_to_array(img) / 255.0  # normalize pixel values
    return np.expand_dims(img_array, axis=0)  # add batch dimension


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/input')
def input_page():
    return render_template('input.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)

    if file:
        filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(image_path)

        img = preprocess_image(image_path)
        predictions = model.predict(img)[0]
        index = np.argmax(predictions)
        confidence = round(predictions[index] * 100, 2)
        label = labels[index]

        return render_template('output.html', label=label, confidence=confidence, image_path='/' + image_path)

if __name__ == '__main__':
    app.run(debug=True)
