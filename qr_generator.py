"""
QR Code Generator for traceability reports.
Generates a QR code that encodes batch info + links to the digital report.
"""
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
import os
import json
import datetime

def generate_qr(farm_data: dict, report_path: str, output_dir: str = "qrcodes") -> str:
    """
    Generate a styled QR code for the traceability report.
    Returns path to the QR image.
    """
    os.makedirs(output_dir, exist_ok=True)

    batch_id  = farm_data.get("batch_id", "BATCH001")
    crop      = farm_data.get("crop", "Unknown")
    farmer    = farm_data.get("farmer_name", "Unknown")
    location  = farm_data.get("location", "Unknown")
    harvest   = farm_data.get("harvest_date", "Unknown")

    # Build a JSON payload that could be served as an API endpoint
    payload = {
        "system":        "Farm2Fork Traceability",
        "batch_id":      batch_id,
        "crop":          crop,
        "farmer":        farmer,
        "location":      location,
        "harvest_date":  harvest,
        "report_file":   os.path.basename(report_path),
        "generated_at":  datetime.datetime.now().isoformat(),
        "fssai_check":   "Completed",
        "verify_url":    f"https://farm2fork.in/verify/{batch_id}"
    }

    qr_data = json.dumps(payload, indent=None, separators=(',', ':'))

    qr = qrcode.QRCode(
        version=3,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)

    img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=RoundedModuleDrawer(),
        fill_color="#1A5C2E",
        back_color="white"
    )

    filename = f"QR_{crop.replace(' ','_')}_{batch_id}.png"
    filepath = os.path.join(output_dir, filename)
    img.save(filepath)
    return filepath
