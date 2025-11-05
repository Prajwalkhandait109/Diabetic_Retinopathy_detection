import os
import numpy as np
from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
from PIL import Image
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# --- Custom Objects ---
class CustomScaleLayer(tf.keras.layers.Layer):
    """Custom layer used by some saved models. Scales inputs by a factor.
    Accepts common aliases in config: 'scale', 'factor', or 'alpha'.
    """
    def __init__(self, scale=1.0, **kwargs):
        # Accept alias keys if present in serialized config
        if 'factor' in kwargs:
            scale = kwargs.pop('factor')
        if 'alpha' in kwargs:
            scale = kwargs.pop('alpha')
        super().__init__(**kwargs)
        self.scale = float(scale)

    def call(self, inputs):
        # Support single tensor or a list/tuple of tensors
        if isinstance(inputs, (list, tuple)):
            # Combine multiple inputs into a single tensor before scaling
            tensors = [tf.convert_to_tensor(inp) for inp in inputs]
            x = tf.add_n(tensors)
            return x * self.scale
        x = tf.convert_to_tensor(inputs)
        return x * self.scale

    # Keras may require output spec/shape inference for custom layers
    def compute_output_shape(self, input_shape):
        # Preserve input shape; if multiple inputs, use the first one's shape
        if isinstance(input_shape, (list, tuple)):
            return input_shape[0]
        return input_shape

    def get_config(self):
        config = super().get_config()
        config.update({'scale': self.scale})
        return config

# Map of custom objects for model deserialization
CUSTOM_OBJECTS = {
    'CustomScaleLayer': CustomScaleLayer,
}

# Load your trained model
def get_model():
    try:
        # Update this path to your actual model file
        model_path = 'model/custom_cnn.h5'
        model = load_model(model_path, custom_objects=CUSTOM_OBJECTS)
        print(f"Model loaded successfully from {model_path}")
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

# Global variable for model
model = get_model()

# Class labels
class_names = ['No DR', 'Mild DR', 'Moderate DR', 'Severe DR', 'Proliferative DR']

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def preprocess_image(img_path, target_size=(100, 100)):
    """Preprocess the image for model prediction with dynamic sizing"""
    try:
        img = Image.open(img_path)
        
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize to target input size
        img = img.resize(target_size)
        
        # Convert to numpy array
        img_array = np.array(img)
        
        # Ensure correct shape (add batch dimension)
        img_array = np.expand_dims(img_array, axis=0)
        
        # Normalize pixel values
        img_array = img_array.astype('float32') / 255.0
        
        return img_array
    except Exception as e:
        print(f"Error preprocessing image: {e}")
        raise e

def get_available_models():
    model_dir = 'model'
    if not os.path.exists(model_dir):
        return []
    return [f for f in os.listdir(model_dir) if f.endswith('.h5')]

@app.route('/')
def index():
    models = get_available_models()
    return render_template('index.html', models=models)

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    model_name = request.form.get('model')

    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            if not model_name:
                return jsonify({'error': 'No model selected'})

            model_path = os.path.join('model', model_name)
            print(f"Loading model from: {model_path}")
            model = load_model(model_path, custom_objects=CUSTOM_OBJECTS)
            
            print("Preprocessing image...")
            # Determine target size from model input shape (None, H, W, C)
            input_shape = getattr(model, 'input_shape', None)
            target_size = (100, 100)
            if input_shape and len(input_shape) == 4:
                h, w = input_shape[1], input_shape[2]
                if isinstance(h, int) and isinstance(w, int) and h > 0 and w > 0:
                    target_size = (w, h)  # PIL expects (width, height)
                    print(f"Detected model input size: {target_size}")

            processed_image = preprocess_image(filepath, target_size=target_size)
            print(f"Image shape: {processed_image.shape}")
            print(f"Image dtype: {processed_image.dtype}")
            
            print("Making prediction...")
            predictions = model.predict(processed_image, verbose=0)
            print(f"Raw predictions: {predictions}")
            
            class_idx = np.argmax(predictions[0])
            confidence = float(predictions[0][class_idx])
            
            result = {
                'prediction': class_names[class_idx],
                'confidence': round(confidence * 100, 2),
                'image_path': f"/static/uploads/{filename}"
            }
            
            print(f"Prediction result: {result}")
            return jsonify(result)
            
        except Exception as e:
            print(f"Error in prediction: {e}")
            import traceback
            traceback.print_exc()
            return jsonify({'error': f'Prediction error: {str(e)}'})
            
    return jsonify({'error': 'Invalid file type'})

if __name__ == '__main__':
    app.run(debug=True)