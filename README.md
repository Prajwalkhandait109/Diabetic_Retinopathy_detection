# Diabetic Retinopathy Detection Web Application

A web-based application for automated diabetic retinopathy detection using deep learning.

## Quick Start (Windows)

- Install Python 3.9+ and Git.
- Clone the repo: `git clone https://github.com/<your-username>/Diabetic_Retinopathy_detection.git`
- In the project folder, run: `./setup.ps1` (PowerShell)
- Start the app: `./run.ps1`
- Open `http://127.0.0.1:5000/` in your browser.

Models are tracked via Git LFS. After cloning, run:

```
git lfs install
git lfs pull
```

If you downloaded a source archive from GitHub and models are missing, use the release ZIP artifact or clone via Git with LFS.

## Project Overview

This application uses a convolutional neural network (CNN) to analyze retinal images and detect signs of diabetic retinopathy, classifying them into five stages:
- No DR
- Mild DR
- Moderate DR
- Severe DR
- Proliferative DR

## System Architecture

The application follows a client-server architecture:
- **Frontend**: HTML, CSS, JavaScript with Bootstrap for responsive design
- **Backend**: Flask Python web server
- **Model**: TensorFlow/Keras CNN for image classification

## Features

- User-friendly interface for image upload
- Real-time image analysis and prediction
- Detailed results with confidence scores
- Educational information about diabetic retinopathy

## Setup and Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

### Installation Steps

1. Clone the repository or download the project files

2. Alternatively to the scripts, create and activate a virtual environment (recommended):
   ```
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Ensure models are present (Git LFS):
   ```
   git lfs install
   git lfs pull
   ```

5. Run the Flask application:
   ```
   python app.py
   ```

6. Open a web browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

## Usage

1. Click the "Select Retinal Image" button to upload a retinal image
2. Click "Analyze Image" to process the image
3. View the results, including:
   - Predicted DR stage
   - Confidence score
   - Information about the detected condition

## Project Structure

```
diabetic-retinopathy-detection/
│
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
│
├── model/
│   ├── dr_model.py         # Script to generate model
│   ├── train_model.py      # Model training script
│   └── dr_model.h5         # Trained model file (generated)
│
├── static/
│   ├── css/
│   │   └── style.css       # Custom CSS styles
│   ├── js/
│   │   └── script.js       # Frontend JavaScript
│   └── uploads/            # Folder for uploaded images
│
└── templates/
    └── index.html          # Main HTML template
```

## Model Information

The deep learning model is a convolutional neural network (CNN) designed to classify retinal images into five stages of diabetic retinopathy. The model architecture includes:

- Multiple convolutional layers for feature extraction
- Max pooling layers for spatial dimension reduction
- Dropout layers to prevent overfitting
- Dense layers for classification

In a production environment, this model would be trained on a large dataset of labeled retinal images.

## Limitations and Future Work

- The current implementation uses a simplified model for demonstration purposes
- For production use, the model should be trained on a large, diverse dataset
- Additional features could include:
  - User accounts and history tracking
  - Integration with electronic health records
  - Mobile application support
  - More detailed analysis and region highlighting

## References

- American Academy of Ophthalmology - Diabetic Retinopathy
- TensorFlow and Keras Documentation
- Flask Web Framework Documentation

## License

This project is for educational purposes only.

## Author

Final Year Project - 2025
## Release Usage

- Download the latest release ZIP from GitHub Releases.
- Extract, open PowerShell, and run `./setup.ps1` to create a virtual environment and install dependencies.
- Run `./run.ps1` to start the app.

## Versioning

- Current version: see `VERSION` file.
- See `RELEASE_NOTES.md` for changes.