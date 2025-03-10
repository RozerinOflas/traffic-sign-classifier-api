from fastapi import FastAPI, File, UploadFile
import torch
from torchvision import transforms
from PIL import Image
import io

# FastAPI uygulamasını başlat
app = FastAPI()

# Modeli yükleme fonksiyonu
def load_model():
    model = torch.load("model/model.pth", map_location=torch.device('cpu'))
    model.eval()
    return model

model = load_model()

# Görüntüyü modele uygun hale getirme
def transform_image(image_bytes):
    transform = transforms.Compose([
        transforms.Resize((32, 32)),
        transforms.ToTensor(),
    ])
    image = Image.open(io.BytesIO(image_bytes))
    return transform(image).unsqueeze(0)

# API endpoint
@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    image_bytes = await file.read()
    img_tensor = transform_image(image_bytes)
    output = model(img_tensor)
    prediction = torch.argmax(output, dim=1).item()
    return {"prediction": prediction}
