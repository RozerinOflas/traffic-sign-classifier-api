# Resmi Python imajını kullan
FROM python:3.9

# Çalışma dizinini ayarla
WORKDIR /app

# Gerekli dosyaları kopyala
COPY requirements.txt .
COPY main.py .


# Gerekli paketleri yükle
RUN pip install --no-cache-dir -r requirements.txt

# API'yi başlat
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7001"]
