import os
from flask import Flask, render_template, request, redirect
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient
import pymysql

# Memuat kunci rahasia dari file .env
load_dotenv()

app = Flask(__name__)

# Konfigurasi koneksi Azure
blob_service_client = BlobServiceClient.from_connection_string(os.getenv("AZURE_CONNECTION_STRING"))
container_name = os.getenv("AZURE_CONTAINER_NAME")

# Fungsi koneksi Database
def get_db_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        ssl={"ssl": {}}
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    # 1. Tangkap data dari form
    nama = request.form['nama']
    email = request.form['email']
    file_ktp = request.files['ktp']

    if file_ktp:
        # 2. Upload gambar ke Azure Object Storage
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_ktp.filename)
        blob_client.upload_blob(file_ktp.read(), overwrite=True)
        
        # Dapatkan URL Publik gambar
        ktp_url = blob_client.url

        # 3. Simpan teks (nama, email) dan URL gambar ke MySQL
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO pelamar (nama, email, ktp_url) VALUES (%s, %s, %s)', (nama, email, ktp_url))
        conn.commit()
        cursor.close()
        conn.close()

        return "<h2>Pendaftaran Berhasil!</h2><p>Data tersimpan di Database dan gambar di Object Storage.</p>"
    
    return "Gagal: File tidak ditemukan."

if __name__ == '__main__':
    app.run(debug=True)