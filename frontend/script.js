document.addEventListener('DOMContentLoaded', () => {
    const dropArea = document.getElementById('drop-area');
    const fileInput = document.getElementById('file-input');
    const browseBtn = document.getElementById('browse-btn');
    const uploadCard = document.getElementById('upload-card');
    const previewCard = document.getElementById('preview-card');
    const imagePreview = document.getElementById('image-preview');
    const resetBtn = document.getElementById('reset-btn');
    const analyzeBtn = document.getElementById('analyze-btn');
    const resultCard = document.getElementById('result-card');
    const loader = document.getElementById('loader');
    const resultContent = document.getElementById('result-content');
    const predictionText = document.getElementById('prediction-text');

    // Slideshow logic
    const slides = document.querySelectorAll('.slide');
    let currentSlide = 0;

    setInterval(() => {
        slides[currentSlide].classList.remove('active');
        currentSlide = (currentSlide + 1) % slides.length;
        slides[currentSlide].classList.add('active');
    }, 8000); // Change background every 8 seconds

    let currentFile = null;

    // Trigger file selection
    browseBtn.addEventListener('click', () => {
        fileInput.click();
    });

    // Handle drag and drop events
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, () => {
            dropArea.classList.add('drag-over');
        }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, () => {
            dropArea.classList.remove('drag-over');
        }, false);
    });

    dropArea.addEventListener('drop', (e) => {
        let dt = e.dataTransfer;
        let files = dt.files;
        handleFiles(files);
    });

    fileInput.addEventListener('change', function() {
        handleFiles(this.files);
    });

    function handleFiles(files) {
        if (files.length > 0) {
            const file = files[0];
            if (file.type.startsWith('image/')) {
                currentFile = file;
                const reader = new FileReader();
                reader.readAsDataURL(file);
                reader.onloadend = function() {
                    imagePreview.src = reader.result;
                    uploadCard.classList.add('hidden');
                    previewCard.classList.remove('hidden');
                    resultCard.classList.add('hidden');
                }
            } else {
                alert('Please upload an image file.');
            }
        }
    }

    resetBtn.addEventListener('click', () => {
        currentFile = null;
        fileInput.value = '';
        previewCard.classList.add('hidden');
        resultCard.classList.add('hidden');
        uploadCard.classList.remove('hidden');
    });

    analyzeBtn.addEventListener('click', async () => {
        if (!currentFile) return;

        // Show loading state
        resultCard.classList.remove('hidden');
        loader.classList.remove('hidden');
        resultContent.classList.add('hidden');
        analyzeBtn.disabled = true;

        const formData = new FormData();
        formData.append('file', currentFile);

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            
            // Display result
            loader.classList.add('hidden');
            resultContent.classList.remove('hidden');
            
            if (data.prediction === 'oil') {
                predictionText.textContent = '⚠️ Oil Spill Detected';
                predictionText.className = 'result-oil';
            } else {
                predictionText.textContent = '✅ No Oil Spill';
                predictionText.className = 'result-no-oil';
            }
            
        } catch (error) {
            console.error('Error:', error);
            loader.classList.add('hidden');
            resultContent.classList.remove('hidden');
            predictionText.textContent = 'Error analyzing image';
            predictionText.className = 'result-oil';
        } finally {
            analyzeBtn.disabled = false;
        }
    });
});
