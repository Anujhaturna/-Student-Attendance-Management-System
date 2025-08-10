import os
import django
import qrcode
from django.conf import settings

# Set the correct settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "student_management_system.settings")
django.setup()

login_url = "http://192.168.80.40:8000/authentication/login/"


# Generate QR Code
qr = qrcode.make(login_url)

# Define the static folder path
static_dir = os.path.join(settings.BASE_DIR, "static")

# Create the static directory if it doesn't exist
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

# Define the QR code file path
qr_path = os.path.join(static_dir, "common_qr.png")

# Save the QR code
qr.save(qr_path)

print(f"QR Code saved at: {qr_path}")





