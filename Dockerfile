# Gunakan image Python versi ringan (Slim)
FROM python:3.10-slim

# Set folder kerja di dalam container
WORKDIR /app

# Copy requirements dan install dulu (agar caching efisien)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy sisa script
COPY . .

# Command default (bisa di-override lewat docker-compose)
CMD ["python", "pddikti.py"]