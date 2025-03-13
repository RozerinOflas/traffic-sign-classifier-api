from fastapi import FastAPI, UploadFile, File
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import uvicorn
from io import BytesIO
from PIL import Image

app = FastAPI()

# Modeli yükleme
model_path = "traffic_sign_classifier.h5"  # Colab'de eğitilen model
model = load_model(model_path)

# Sınıf isimleri
class_names = [ "Speed limit (20km/h)", "Speed limit (30km/h)", "Speed limit (50km/h)", 
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
]  # Örnek sınıflar

@app.get("/")
def home():
    return {"message": "Traffic Sign Classifier API is running."}

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    # Görüntüyü okuma
    contents = await file.read()
    image_data = Image.open(BytesIO(contents)).convert("RGB")
    image_data = image_data.resize((30, 30))  # Modelin beklediği boyuta getirme

    # Görüntüyü numpy dizisine çevirme
    img_array = image.img_to_array(image_data)
    img_array = np.expand_dims(img_array, axis=0)

    # Model ile tahmin yapma
    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions)
    confidence = np.max(predictions)

    return {
        "predicted_class": class_names[predicted_class],
        "confidence": float(confidence)
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7001)
