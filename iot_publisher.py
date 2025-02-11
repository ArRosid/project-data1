import boto3
import json
import time
import random
from decimal import Decimal

# Konfigurasi
S3_BUCKET_NAME = "your-s3-bucket-name"  # Ganti dengan nama bucket S3 Anda
S3_FILE_NAME = "events.json"

# Inisialisasi klien S3
s3_client = boto3.client("s3")

# Fungsi untuk membuat data event random
def generate_event():
    return {
        "device_id": f"device-{random.randint(1, 100)}",
        "event_type": random.choice(["temperature", "humidity", "motion"]),
        "value": int(Decimal(random.randint(1000, 10000)) / 100),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }

# Membuat 100 data event
events = [generate_event() for _ in range(100)]

# Simpan ke file JSON
with open("events.json", "w") as f:
    json.dump(events, f, indent=2)

# Unggah ke S3
try:
    s3_client.upload_file("events.json", S3_BUCKET_NAME, S3_FILE_NAME)
    print(f"✅ File {S3_FILE_NAME} berhasil diunggah ke S3 bucket {S3_BUCKET_NAME}")
except Exception as e:
    print(f"❌ Gagal mengunggah ke S3: {e}")
