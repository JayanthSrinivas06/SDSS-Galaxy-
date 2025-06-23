from flask import Flask, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a random secret key

# Configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'webp'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    """Home page route"""
    return render_template('home.html')

@app.route('/input')
def input_page():
    """Input/upload page route"""
    return render_template('input.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and redirect to results"""
    if 'galaxy_image' not in request.files:
        flash('No file selected')
        return redirect(url_for('input_page'))
    
    file = request.files['galaxy_image']
    
    if file.filename == '':
        flash('No file selected')
        return redirect(url_for('input_page'))
    
    if file and allowed_file(file.filename):
        # Generate unique filename to avoid conflicts
        filename = str(uuid.uuid4()) + '.' + file.filename.rsplit('.', 1)[1].lower()
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Get form data
        confidence = request.form.get('confidence', '0.7')
        model = request.form.get('model', 'cnn_v2')
        
        # Redirect to results page with parameters
        return redirect(url_for('output_page', 
                              filename=filename, 
                              confidence=confidence, 
                              model=model))
    else:
        flash('Invalid file type. Please upload an image file.')
        return redirect(url_for('input_page'))

@app.route('/output')
def output_page():
    """Results/output page route"""
    # Get parameters from URL
    filename = request.args.get('filename', '')
    confidence = request.args.get('confidence', '0.7')
    model = request.args.get('model', 'cnn_v2')
    
    # In a real application, you would process the image here
    # For now, we'll pass the parameters to the template
    return render_template('output.html', 
                         uploaded_image=filename,
                         confidence_threshold=confidence,
                         selected_model=model)

@app.route('/classify')
def classify_redirect():
    """Redirect /classify to input page for compatibility"""
    return redirect(url_for('input_page'))

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    flash('File is too large. Maximum size is 16MB.')
    return redirect(url_for('input_page'))

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors"""
    return render_template('home.html'), 404

if __name__ == '__main__':
    print("🌌 Starting SDSS Galaxy Classification Server...")
    print("📡 Server running at: http://localhost:5000")
    print("🚀 Navigate to the URL above to start classifying galaxies!")
    app.run(debug=True, host='0.0.0.0', port=5000)