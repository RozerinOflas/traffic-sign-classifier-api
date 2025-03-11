# Python 3.8 imajını kullanıyoruz
FROM python:3.9

# Çalışma dizinini belirliyoruz
WORKDIR /app

# Gereksinim dosyasını çalışma dizinine kopyalayalım
COPY requirements.txt .

# Gereksinimlerinizi yükleyin
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyalarını kopyalayalım
COPY . .

EXPOSE 7001

# FastAPI uygulamasını çalıştıran komut
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7001"]
