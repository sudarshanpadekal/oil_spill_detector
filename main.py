import io
import tempfile
from pathlib import Path

import os
import random
from datetime import datetime
from twilio.rest import Client
from fpdf import FPDF

import cv2
import torch
from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from PIL import Image
from dotenv import load_dotenv

load_dotenv()
from torchvision import models, transforms
from ultralytics import YOLO
from ultralytics.utils.plotting import colors

# Change truecolor (class 2) mask color from grey to bright orange
colors.palette[2] = (255, 165, 0)

app = FastAPI()

model = models.resnet18(weights = None)
model.fc = torch.nn.Linear(model.fc.in_features, 2)
model.load_state_dict(torch.load("oil_model.pth", map_location='cpu', weights_only=True))

model.eval()

yolo_model = YOLO("models/best.pt")

classes = ["no_oil","oil"]

# In-memory storage for the Dashboard Analytics
dashboard_data = {
    "total_scans": 142, # Mock starting point
    "spills_found": 37,
    "recent_detections": [],
    "historical": {
        "labels": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        "data": [12, 19, 8, 15, 22, 5]
    }
}

def generate_pdf_report(confidence: float, timing_seconds: float, lat: float, lng: float, snapshot_path: Path = None) -> str:
    reports_dir = Path("outputs/reports")
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"incident_report_{timestamp_str}.pdf"
    filepath = reports_dir / filename
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="SARVision Incident Report", ln=True, align='C')
    
    pdf.set_font("Arial", '', 12)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Date/Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.cell(200, 10, txt=f"Detection Type: Oil Spill", ln=True)
    pdf.cell(200, 10, txt=f"Confidence Score: {confidence*100:.2f}%", ln=True)
    pdf.cell(200, 10, txt=f"Detection Timing: {timing_seconds:.2f} seconds into footage", ln=True)
    pdf.cell(200, 10, txt=f"GPS Coordinates (Mocked): {lat:.4f}, {lng:.4f}", ln=True)
    
    pdf.ln(10)
    if snapshot_path and snapshot_path.exists():
        pdf.image(str(snapshot_path), x=30, w=150)
    else:
        pdf.set_font("Arial", 'I', 10)
        pdf.multi_cell(0, 10, txt="Note: Visual snapshot not available.")
    
    pdf.output(str(filepath))
    return f"/outputs/reports/{filename}"

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.Grayscale(num_output_channels=3),
    transforms.ToTensor(),
    transforms.Normalize([0.5,0.5,0.5], [0.5,0.5,0.5])
])



@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert('RGB')

    image = transform(image).unsqueeze(0)

    with torch.no_grad():
        outputs = model(image)
        _, pred = torch.max(outputs, 1)

    return {
        "prediction": classes[pred.item()]
    }


# Removed convert_avi_to_mp4 to speed up processing


def process_video_background(input_path: Path, output_dir: Path):
    try:
        cap = cv2.VideoCapture(str(input_path))
        fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
        cap.release()

        results = yolo_model.predict(
            source=str(input_path),
            save=False,
            vid_stride=3,
            stream=True
        )

        max_conf = 0.0
        frame_idx_of_max = 0
        current_frame = 0
        best_frame_bgr = None

        for r in results:
            if r.boxes and len(r.boxes.conf) > 0:
                frame_max = float(torch.max(r.boxes.conf))
                if frame_max > max_conf:
                    max_conf = frame_max
                    frame_idx_of_max = current_frame
                    best_frame_bgr = r.plot()
            current_frame += 1

        original_frame = frame_idx_of_max * 3
        timing_seconds = original_frame / fps
        
        dashboard_data["total_scans"] += 1
        pdf_url = ""
        snapshot_url = ""

        if max_conf > 0:
            dashboard_data["spills_found"] += 1
            
            # Save the snapshot
            snapshot_path = None
            if best_frame_bgr is not None:
                timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
                snapshot_filename = f"snapshot_{timestamp_str}.jpg"
                snapshot_path = Path("outputs/reports") / snapshot_filename
                cv2.imwrite(str(snapshot_path), best_frame_bgr)
                snapshot_url = f"/outputs/reports/{snapshot_filename}"
            
            # Mock Ocean Coordinates
            lat = random.uniform(-40.0, 40.0)
            lng = random.uniform(-180.0, 180.0)
            
            pdf_url = generate_pdf_report(max_conf, timing_seconds, lat, lng, snapshot_path)
            
            dashboard_data["recent_detections"].insert(0, {
                "id": str(random.randint(1000, 9999)),
                "lat": lat,
                "lng": lng,
                "confidence": max_conf,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "pdf_url": pdf_url,
                "snapshot_url": snapshot_url
            })
            
            # Keep list short
            if len(dashboard_data["recent_detections"]) > 10:
                dashboard_data["recent_detections"].pop()

        twilio_sid = os.getenv("TWILIO_ACCOUNT_SID")
        twilio_auth = os.getenv("TWILIO_AUTH_TOKEN")
        twilio_phone = os.getenv("TWILIO_PHONE_NUMBER")
        target_phone = "whatsapp:+916363469218"

        if twilio_sid and twilio_auth and twilio_phone and max_conf > 0:
            try:
                client = Client(twilio_sid, twilio_auth)
                message_body = (
                    f"SARVision Alert: Oil spill detected!\n"
                    f"Time detected: {timing_seconds:.2f} seconds\n"
                    f"Confidence score: {max_conf*100:.2f}%\n"
                    f"Snapshot: http://localhost:8000{snapshot_url}\n"
                    f"Report: http://localhost:8000{pdf_url}"
                )
                
                message = client.messages.create(
                    body=message_body,
                    from_=twilio_phone,
                    to=target_phone
                )
                print(f"Sent SMS alert! SID: {message.sid}")
            except Exception as e:
                print(f"Failed to send SMS: {e}")

    except Exception as e:
        print(f"Background processing error: {e}")
    finally:
        if input_path.exists():
            input_path.unlink(missing_ok=True)

@app.post("/video-detect")
async def video_detect(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")

    uploads_dir = Path("uploads")
    outputs_dir = Path("outputs/videos")
    uploads_dir.mkdir(exist_ok=True)
    outputs_dir.mkdir(exist_ok=True)

    suffix = Path(file.filename).suffix or ".mp4"
    temp_input_path = Path(tempfile.NamedTemporaryFile(dir=uploads_dir, suffix=suffix, delete=False).name)

    contents = await file.read()
    temp_input_path.write_bytes(contents)

    background_tasks.add_task(process_video_background, temp_input_path, outputs_dir)

    return {
        "status": "success",
        "message": "Video uploaded successfully. Processing in background. An SMS alert will be sent to +916363469218 when finished."
    }

@app.get("/api/stats")
async def get_stats():
    return dashboard_data

app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")