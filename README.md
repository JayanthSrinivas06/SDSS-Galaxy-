# 🌌 SDSS Galaxy Classification Web App

This project is a Flask-based web application that uses a Convolutional Neural Network (CNN) to classify galaxies from images into 5 categories. It is trained using a dataset from Kaggle and deployed locally for interactive predictions.

---

## 📁 Project Structure

```
.
├── static/
│   ├── style.css
│   └── uploads/                       ← (Create this folder manually after training)
├── templates/
│   ├── home.html
│   ├── input.html
│   └── output.html
├── training/
│   ├── Galaxy_Dataset
|       ├── test
|       ├── train
|       └── val
│   ├── Train_dataset
|       ├── Cigar-shaped smooth
|       ├── completely rounf=d smooth
|       ├── edge-on
|       ├── In between smooth
|       └── spiral
│   └── sdss.ipynb                     ← Jupyter notebook to train and save the model
├── SDSSmodel.h5                           ← Saved model after training
├── run.py                             ← Flask web server
├── README.md                          ← This file
```

---

## 📦 Dataset Preparation

Download the dataset from Kaggle:  
🔗 [Galaxy Zoo - The Galaxy Classification Dataset](https://www.kaggle.com/datasets)

- Ensure your dataset contains **exactly 5 classes** corresponding to:
  - `Cigar-shaped smooth`
  - `In between smooth`
  - `Completely round smooth`
  - `Edge-on`
  - `Spiral`

Organize the dataset in this format:

```
galaxy_dataset/
├── cigar-shaped smooth/
├── in between smooth/
├── completely round smooth/
├── edge-on/
└── spiral/
```

---

## 🧠 Step 1: Train and Save the Model

1. Open `sdss.ipynb` in Jupyter Notebook or Google Colab.
2. Update the dataset path in the notebook if necessary.
3. Train your model using TensorFlow or Keras.
4. Save the trained model using:

```python
model.save('model.h5')
```

5. Move the `model.h5` file into your project root directory (same as `run.py`).

---

## 📂 Step 2: Create Uploads Folder

Create an empty `uploads` directory inside the `static` folder to store uploaded images:

```bash
mkdir static/uploads
```

---

## ▶️ Step 3: Run the App Locally

### 1. Install dependencies:

```bash
pip install flask tensorflow pillow numpy
```

### 2. Run the Flask server:

```bash
python run.py
```

### 3. Open your browser and go to:

```
http://127.0.0.1:5000/
```

You’ll be taken to the home page with a “Start Classification” button.

---

## 📄 HTML Pages

- `home.html` – Starting page with a navigation button
- `input.html` – Upload an image
- `output.html` – View the prediction and confidence score

---

## 🛠 Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS
- **ML Framework**: TensorFlow / Keras
- **Model Format**: `.h5`

---

## ❗ Notes

- Only image files (`.jpg`, `.jpeg`, `.png`) are supported.
- The model input size used in preprocessing (e.g., `(150, 150)`) must match what was used during training.
- The app assumes classification into exactly 5 galaxy types.

---

## 📬 Contact

Maintained by **Jayanth Srinivas Bommisetty**  
For questions or feedback, feel free to raise an issue on GitHub or Gmail: jayanth.b.cse@gmail.com.

---
