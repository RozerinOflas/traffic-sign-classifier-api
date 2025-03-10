from fastapi import FastAPI, File, UploadFile
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import io

app = FastAPI()

# Modeli yükle
model = load_model("traffic_sign_classifier.h5")

# Sınıf isimleri (0-indexli olmalı!)
class_names = [
    "Speed limit (20km/h)", "Speed limit (30km/h)", "Speed limit (50km/h)", 
    "Speed limit (60km/h)", "Speed limit (70km/h)", "Speed limit (80km/h)", 
    "End of speed limit (80km/h)", "Speed limit (100km/h)", "Speed limit (120km/h)", 
    "No passing", "No passing veh over 3.5 tons", "Right-of-way at intersection", 
    "Priority road", "Yield", "Stop", "No vehicles", "Veh > 3.5 tons prohibited", 
    "No entry", "General caution", "Dangerous curve left", "Dangerous curve right", 
    "Double curve", "Bumpy road", "Slippery road", "Road narrows on the right", 
    "Road work", "Traffic signals", "Pedestrians", "Children crossing", "Bicycles crossing", 
    "Beware of ice/snow", "Wild animals crossing", "End speed + passing limits", 
    "Turn right ahead", "Turn left ahead", "Ahead only", "Go straight or right", 
    "Go straight or left", "Keep right", "Keep left", "Roundabout mandatory", 
    "End of no passing", "End no passing veh > 3.5 tons"
]

@app.get("/")
def home():
    return {"message": "Traffic Sign Classifier API is running!"}

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    try:
        # Görüntüyü oku ve modele uygun hale getir
        image = Image.open(io.BytesIO(await file.read()))
        image = image.resize((30, 30))  # Modelin beklediği giriş boyutu
        image_array = np.array(image) / 255.0  # Normalizasyon
        image_array = np.expand_dims(image_array, axis=0)  # Modelin beklediği şekle getir
        
        # Model ile tahmin yap
        predictions = model.predict(image_array)
        predicted_class = np.argmax(predictions)  # En yüksek olasılığa sahip sınıfı al
        confidence = float(np.max(predictions))  # Olasılık değeri
        
        return {"class": class_names[predicted_class], "confidence": confidence}
    
    except Exception as e:
        return {"error": str(e)}
