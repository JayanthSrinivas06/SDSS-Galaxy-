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
        img_bytes = file.read()

        from PIL import Image
        from io import BytesIO

        img = Image.open(BytesIO(img_bytes)).convert("RGB")  # ensure 3-channel
        img = img.resize((256, 256))  # resize to model input size

        img_array = img_to_array(img)
        input_array = np.expand_dims(img_array, axis=0)

        # Predict
        predictions = model.predict(input_array)[0]
        index = np.argmax(predictions)
        confidence = round(predictions[index] * 100, 2)
        label = labels[index]

        # Save image with predicted label as filename
        ext = os.path.splitext(file.filename)[1] or '.jpg'
        filename = f"{label}_{uuid.uuid4()}{ext}"
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        img.save(image_path)

        return render_template('output.html', label=label, confidence=confidence, image_path='/' + image_path)



if __name__ == '__main__':
    app.run(debug=True)
