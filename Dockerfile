# Gunakan sistem operasi Python 3.11 versi ringan sebagai fondasi
FROM python:3.11-slim

# Tentukan ruang kerja di dalam kontainer
WORKDIR /app

# Salin file requirements.txt dan install semua library-nya
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Salin seluruh kode aplikasimu (app.py, templates/, dll) ke dalam kontainer
COPY . .

# Buka port 5000 agar aplikasi bisa diakses dari luar
EXPOSE 5000

# Perintah wajib untuk menyalakan server Flask di dalam Docker
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]