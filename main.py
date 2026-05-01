import torch
from torchvision import transforms, models
from fastapi import FastAPI, UploadFile, File
from PIL import Image
import io

app = FastAPI()

model = models.resnet18(weights = None)
model.fc = torch.nn.Linear(model.fc.in_features, 2)
model.load_state_dict(torch.load("oil_model.pth", map_location='cpu', weights_only=True))

model.eval()

classes = ["no_oil","oil"]

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.Grayscale(num_output_channels=3),
    transforms.ToTensor(),
    transforms.Normalize([0.5,0.5,0.5], [0.5,0.5,0.5])
])

@app.get('/')
def home():
    return {"message": "Oil Spill Detection API is running"}

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