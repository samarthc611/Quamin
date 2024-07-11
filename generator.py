from flask import Flask
from pymongo import MongoClient
import os
import qrcode

app = Flask(__name__)


client = MongoClient("mongodb+srv://220010052:KC09AxTI9vP555Vh@cluster0.fmo3c2z.mongodb.net/")
db = client.certificates  
collection = db.all_certificates  

base_url = "https://quamin.onrender.com/verify?cert_id="

documents = collection.find()
for doc in documents:
    cert_id = str(doc['_id'])

    verification_url = base_url + cert_id

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(verification_url)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')

    file_path = os.path.join(os.getcwd(), f"certificate_qr_code_{cert_id}.png")
    img.save(file_path)

    print(f"QR code generated and saved as {file_path}")