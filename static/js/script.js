document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('upload-form');
    const imageUpload = document.getElementById('image-upload');
    const predictBtn = document.getElementById('predict-btn');
    const resultsSection = document.getElementById('results-section');
    const resultImage = document.getElementById('result-image');
    const predictionResult = document.getElementById('prediction-result');
    const confidenceBar = document.getElementById('confidence-bar');
    const confidenceText = document.getElementById('confidence-text');
    const drDescription = document.getElementById('dr-description');

    // DR descriptions for each class
    const drDescriptions = {
        'No DR': 'No signs of diabetic retinopathy detected. Regular eye check-ups are still recommended for diabetic patients.',
        'Mild DR': 'Mild non-proliferative diabetic retinopathy. Small areas of balloon-like swelling in the retina\'s tiny blood vessels.',
        'Moderate DR': 'Moderate non-proliferative diabetic retinopathy. More extensive damage to retinal blood vessels.',
        'Severe DR': 'Severe non-proliferative diabetic retinopathy. Many blood vessels are blocked, depriving several areas of the retina of blood supply.',
        'Proliferative DR': 'Proliferative diabetic retinopathy. The most advanced stage where new, abnormal blood vessels grow in the retina. Urgent medical attention required.'
    };

    // Handle form submission
    uploadForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const file = imageUpload.files[0];
        if (!file) {
            alert('Please select an image to upload');
            return;
        }

        // Check file type
        const validTypes = ['image/jpeg', 'image/jpg', 'image/png'];
        if (!validTypes.includes(file.type)) {
            alert('Please upload a valid image file (JPG, JPEG, or PNG)');
            return;
        }

        // Check file size (max 5MB)
        if (file.size > 5 * 1024 * 1024) {
            alert('File size exceeds 5MB. Please upload a smaller image.');
            return;
        }

        // Show loading state
        predictBtn.disabled = true;
        predictBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Analyzing...';
        
        // Create form data and send request
        const formData = new FormData();
        formData.append('file', file);
        formData.append('model', document.getElementById('model-select').value);

        fetch('/predict', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }
            
            // Display results
            resultImage.src = data.image_path;
            predictionResult.textContent = data.prediction;
            
            // Set confidence bar
            const confidence = parseFloat(data.confidence) * 100;
            confidenceBar.style.width = confidence + '%';
            confidenceText.textContent = confidence.toFixed(1) + '%';
            
            // Set description
            drDescription.textContent = drDescriptions[data.prediction] || 
                'Analysis complete. Please consult with a healthcare professional for interpretation.';
            
            // Apply color coding based on severity
            predictionResult.className = 'fs-5 fw-bold';
            if (data.prediction === 'No DR') {
                predictionResult.classList.add('low-risk');
            } else if (data.prediction === 'Mild DR' || data.prediction === 'Moderate DR') {
                predictionResult.classList.add('medium-risk');
            } else {
                predictionResult.classList.add('high-risk');
            }
            
            // Show results section
            resultsSection.style.display = 'block';
            
            // Scroll to results
            resultsSection.scrollIntoView({ behavior: 'smooth' });
        })
        .catch(error => {
            alert('Error: ' + error.message);
            console.error('Error:', error);
        })
        .finally(() => {
            // Reset button state
            predictBtn.disabled = false;
            predictBtn.innerHTML = 'Analyze Image';
        });
    });

    // Preview image before upload
    imageUpload.addEventListener('change', function() {
        const file = this.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                resultImage.src = e.target.result;
                resultsSection.style.display = 'none'; // Hide previous results
            };
            reader.readAsDataURL(file);
        }
    });
});