# 🌊 SARVision: Oil Spill Detection System

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![PyTorch](https://img.shields.io/badge/PyTorch-Deep%20Learning-ee4c2c)
![FastAPI](https://img.shields.io/badge/FastAPI-Web%20API-009688)
![YOLO](https://img.shields.io/badge/YOLO-Video%20Detection-00A4EF)
![License](https://img.shields.io/badge/License-MIT-green)

An end-to-end deep learning system for detecting oil spills from satellite imagery using ResNet18 image classification and YOLO-based video analysis. Includes a full-stack web application with a FastAPI backend and interactive frontend dashboard.

## 🎯 Overview

**SARVision** combines multiple AI models to detect oil spill activity from different data sources:

- **Image Detection**: Binary classifier (ResNet18) for single image analysis
- **Video Detection**: YOLO-based pipeline for frame-by-frame video scanning
- **Analytics Dashboard**: Real-time monitoring with map visualization and PDF report generation
- **SMS Alerts**: Optional Twilio integration for instant notifications

## ✨ Features

- **Transfer Learning**: ResNet18 pre-trained weights for robust feature extraction
- **Image Classification**: Binary oil/no-oil classification with 88.63% accuracy
- **Video Analysis**: Frame-by-frame YOLO detection with confidence tracking
- **Web API**: FastAPI endpoints for image/video prediction and analytics
- **Interactive UI**: Modern frontend with:
  - Image upload and classification
  - Video upload and processing
  - Global analytics dashboard with live map
  - PDF incident report generation
- **Automated Alerting**: Optional Twilio SMS/WhatsApp notifications
- **Data Augmentation**: Grayscale conversion, resizing, and normalization
- **Model Evaluation**: Comprehensive metrics (Accuracy, Precision, Recall, F1-Score)

## 📁 Repository Structure

```
oil_spill_detector/
├── main.py                      # FastAPI application (entry point)
├── train.py                     # Training pipeline
├── evaluate.py                  # Model evaluation script
├── model.py                     # Model architecture definitions
├── dataset_loader.py            # Dataset loading utilities
├── training_loop.py             # Training loop implementation
├── requirements.txt             # Python dependencies
├── render.yaml                  # Render deployment config
├── oil_model.pth                # Pre-trained ResNet18 weights
├── dataset/
│   ├── oil/                     # Oil spill images
│   └── no_oil/                  # Non-oil images
├── models/
│   └── best.pt                  # YOLO model for video detection
├── frontend/                    # Web UI (served by FastAPI)
│   ├── index.html               # Landing page
│   ├── picture.html             # Image detection page
│   ├── video.html               # Video detection page
│   ├── dashboard.html           # Analytics dashboard
│   ├── script.js                # Image page logic
│   ├── video.js                 # Video page logic
│   ├── dashboard.js             # Dashboard map & charts
│   ├── style.css                # Styling
│   └── assets/                  # Images and media
├── outputs/
│   ├── videos/                  # Processed video outputs
│   └── reports/                 # Generated PDF reports
└── uploads/                     # Temporary video uploads
```

## 🚀 Quick Start

### 1. Clone & Install

```bash
git clone <your-repo-url>
cd oil_spill_detector
pip install -r requirements.txt
```

### 2. Prepare Dataset

Organize images in a `dataset/` folder:
```
dataset/
├── oil/
│   ├── 1/
│   │   ├── image1.jpg
│   │   └── ...
└── no_oil/
    ├── 0/
    │   ├── image1.jpg
    │   └── ...
```

### 3. Train the Model

```bash
python train.py
```

This will:
- Load images from `dataset/`
- Split data into 80% training / 20% validation
- Train ResNet18 for 5 epochs
- Save weights to `oil_model.pth`

### 4. Evaluate Performance

```bash
python evaluate.py
```

### 5. Run the Web Application

```bash
uvicorn main:app --reload
```

Then open [http://localhost:8000](http://localhost:8000) in your browser.

## 🔌 API Endpoints

### Image Prediction
```http
POST /predict
Content-Type: multipart/form-data

file: <image_file>
```

**Response:**
```json
{
  "prediction": "oil"  // or "no_oil"
}
```

### Video Detection
```http
POST /video-detect
Content-Type: multipart/form-data

file: <video_file>
```

**Response:**
```json
{
  "status": "success",
  "message": "Video uploaded successfully. Processing in background. An SMS alert will be sent to +916363469218 when finished."
}
```

### Dashboard Analytics
```http
GET /api/stats
```

**Response:**
```json
{
  "total_scans": 142,
  "spills_found": 37,
  "recent_detections": [
    {
      "id": "1234",
      "lat": 15.5,
      "lng": -120.3,
      "confidence": 0.95,
      "timestamp": "2026-06-22 14:30:15",
      "pdf_url": "/outputs/reports/incident_report_20260622_143015.pdf",
      "snapshot_url": "/outputs/reports/snapshot_20260622_143015.jpg"
    }
  ],
  "historical": {
    "labels": ["Jan", "Feb", "Mar", ...],
    "data": [12, 19, 8, ...]
  }
}
```

## 🎨 Frontend Pages

- **`/` (index.html)**: Landing page with navigation to detection modes
- **`/picture.html`**: Image classification interface
- **`/video.html`**: Video upload and processing
- **`/dashboard.html`**: Real-time analytics with Leaflet map and Chart.js visualizations

## 📊 Model Performance

Trained ResNet18 on binary classification task:

| Metric | Value |
|--------|-------|
| Accuracy | 88.63% |
| Precision | 93.79% |
| Recall | 71.20% |
| F1 Score | 80.95% |

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Twilio SMS/WhatsApp Alerts (optional)
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890

# Recipient phone for alerts (WhatsApp format)
# Currently hardcoded: whatsapp:+916363469218
```

### Model & YOLO Paths

Update in `main.py` if needed:
```python
model.load_state_dict(torch.load("oil_model.pth", map_location='cpu', weights_only=True))
yolo_model = YOLO("models/best.pt")
```

## 📦 Requirements

- Python 3.8+
- PyTorch & TorchVision (CPU or GPU)
- FastAPI & Uvicorn
- OpenCV (headless)
- YOLOv8 (Ultralytics)
- Pillow
- scikit-learn
- python-dotenv
- Twilio SDK (optional)
- fpdf2 (PDF generation)

Install all dependencies:
```bash
pip install -r requirements.txt
```

## 🌐 Deployment on Render

### Prerequisites
- GitHub account with repo pushed
- Render account ([render.com](https://render.com))

### Steps

1. **Create `render.yaml`** (already included in this repo)
2. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Add Render deployment config"
   git push
   ```

3. **Deploy on Render**:
   - Go to [dashboard.render.com](https://dashboard.render.com)
   - Click **"New +"** → **"Web Service"**
   - Connect your GitHub repository
   - Select the branch (usually `main`)
   - Render will auto-detect `render.yaml` configuration
   - Deploy!

4. **Set Environment Variables** in Render Dashboard:
   - Navigate to your service settings
   - Add `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_PHONE_NUMBER` if using SMS alerts

### ⚠️ Important Deployment Notes

- **Model Size**: Ensure `oil_model.pth` and `models/best.pt` are not too large (>50MB combined). If they are, consider:
  - Uploading to Hugging Face Model Hub
  - Using S3 bucket
  - Compressing or quantizing models
  
- **Build Time**: Video processing and YOLO can be heavy. On free tier, builds might timeout.

- **Storage**: Render's free tier doesn't persist files. Generated reports and videos are temporary.

- **Free Tier Limits**:
  - 750 compute hours/month
  - Spins down after 15 mins of inactivity
  - No persistent storage
  
- **Recommended**: Upgrade to a paid Render plan for production use.

## 📝 Usage Examples

### Command Line

**Train a model from scratch:**
```bash
python train.py
```

**Evaluate existing model:**
```bash
python evaluate.py
```

**Start API server:**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Web UI

1. Open [http://localhost:8000](http://localhost:8000)
2. Choose detection mode:
   - **Image**: Upload satellite image, get instant oil/no-oil classification
   - **Video**: Upload video clip, background processing scans frames
   - **Dashboard**: Monitor detections on map with PDF reports

## 🎓 Architecture

### Image Classification Pipeline
```
Input Image → Resize (224×224) → Grayscale → Normalize → ResNet18 → Binary Classification
```

### Video Detection Pipeline
```
Input Video → Extract Frames (stride=3) → YOLO Detection → Track Max Confidence
                                         → Generate PDF Report
                                         → Send SMS Alert (optional)
                                         → Update Dashboard
```

## 🔍 Troubleshooting

### Model not loading
- Ensure `oil_model.pth` is in the root directory
- Check file permissions

### YOLO model not found
- Ensure `models/best.pt` exists
- Download from Hugging Face or train your own

### Twilio alerts not sending
- Verify `.env` file has correct credentials
- Check phone number format (WhatsApp: `whatsapp:+1234567890`)

### Render deployment timeout
- Split large model files
- Use lighter model architectures
- Increase Render plan tier

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## 📧 Contact

For questions or support, please reach out via GitHub issues.
