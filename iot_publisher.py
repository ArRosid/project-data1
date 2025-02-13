import boto3
import csv
import time
import random
from decimal import Decimal

# Konfigurasi
S3_BUCKET_NAME = "project-bucket-source-rosid"  # Ganti dengan nama bucket S3 Anda
S3_FILE_NAME = "events.csv"

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

# Simpan ke file CSV
csv_headers = ["device_id", "event_type", "value", "timestamp"]
with open("events.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=csv_headers)
    writer.writeheader()
    writer.writerows(events)

# Unggah ke S3
try:
    s3_client.upload_file("events.csv", S3_BUCKET_NAME, S3_FILE_NAME)
    print(f"✅ File {S3_FILE_NAME} berhasil diunggah ke S3 bucket {S3_BUCKET_NAME}")
except Exception as e:
    print(f"❌ Gagal mengunggah ke S3: {e}")
