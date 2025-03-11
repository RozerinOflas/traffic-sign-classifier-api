# Küçük ve optimize edilmiş Python 3.9 imajı
FROM python:3.9-slim  

# Çalışma dizini oluştur
WORKDIR /app  

# Bağımlılıkları kopyala ve yükle (Cache avantajı için sırayla yapılıyor)
COPY requirements.txt .  
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt  

# Uygulama dosyalarını kopyala
COPY . .  

# Uvicorn'u optimize etmek için ayarları belirle
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4", "--timeout-keep-alive", "60"]
