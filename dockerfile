# Temel imaj olarak Python kullanıyoruz
FROM python:3.10-slim

# Çalışma dizinini oluştur
WORKDIR /app

# Gereksinimleri kopyala ve yükle
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Uygulama dosyalarını kopyala
COPY . .

# Uygulamayı çalıştır
CMD ["python", "app.py"]
