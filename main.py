from fastapi import FastAPI, File, UploadFile
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import io
from PIL import Image

# FastAPI uygulaması başlatılıyor
app = FastAPI()

# Eğitilmiş model yükleniyor
model = tf.keras.models.load_model("traffic_sign_classifier.h5")

# Sınıf isimleri 
class_names = [    "Speed limit (20km/h)", "Speed limit (30km/h)", "Speed limit (50km/h)", 
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
    return {"message": "FastAPI is running!"}

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    # Görüntüyü açma ve modele uygun boyuta getirme
    contents = await file.read()
    img = Image.open(io.BytesIO(contents))
    img = img.resize((32, 32))  # Modelinizin giriş boyutuna uygun olacak şekilde ayarlayın
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0  # Normalizasyon

    # Modelden tahmin al
    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions)
    confidence = np.max(predictions)

    return {
        "predicted_class": class_names[predicted_class],
        "confidence": float(confidence)
    }
