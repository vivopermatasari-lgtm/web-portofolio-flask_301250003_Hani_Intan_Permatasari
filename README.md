# Web Portofolio Dinamis dengan Python Flask

Capstone project untuk mata kuliah Pengantar Pemrograman.

## Deskripsi

Aplikasi web portofolio pribadi dengan dashboard admin yang memungkinkan mengelola konten proyek, profil, dan pesan masuk secara dinamis tanpa perlu mengubah kode program.

## Fitur Utama

### Halaman Publik (tanpa login)
- **Home**: foto profil, nama, headline/tagline, ringkasan about, navigasi
- **About**: deskripsi diri, pendidikan, skill (dinamis dari database)
- **Portofolio**: daftar proyek dari database (thumbnail, judul, deskripsi singkat, teknologi, link GitHub/live)
- **Detail Proyek**: halaman detail per proyek
- **Kontak**: form (nama, email, pesan) tersimpan ke database + info kontak pemilik

### Dashboard Admin (setelah login)
- **Login/Logout** pakai Flask session, redirect ke login jika belum masuk
- **Ringkasan dashboard**: total proyek, pesan belum dibaca, shortcut fitur
- **CRUD Proyek lengkap**: create (form + upload gambar), read (tabel), update, delete (dengan konfirmasi)
- **Upload gambar**: validasi tipe file (PNG/JPG/JPEG/GIF/WEBP) di sisi server, simpan ke `static/uploads/`, maksimal 5 MB
- **Manajemen profil**: nama, headline, about, foto, skill (tambah/hapus dinamis)
- **Kotak masuk pesan**: tandai dibaca / hapus

## Struktur Proyek

```
web_portofolio/
├── app.py
├── config.py
├── models.py
├── requirements.txt
├── .gitignore
├── README.md
├── dashboard.py
├── static/
│   ├── css/
│   │   └── base.css
│   ├── js/
│   │   └── main.js
│   └── uploads/          (di‑gitignore, dibuat otomatis saat pertama kali dijalankan)
└── templates/
    ├── base.html
    ├── index.html
    ├── about.html
    ├── portfolio.html
    ├── project_detail.html
    ├── contact.html
    └── dashboard/
        ├── login.html
        ├── index.html
        ├── projects.html
        ├── add_project.html
        ├── edit_project.html
        ├── profile.html
        └── messages.html
```

## Pryarat dan Instalasi

1. **Clone repository**
   ```bash
   git clone <repo-url>
   cd web_portofolio
   ```

2. **Buat virtual environment** (disarankan)
   ```bash
   python -m venv venv
   # Linux/macOS
   source venv/bin/activate
   # Windows
   venv\Scripts\activate
   ```

3. **Instal dependensi**
   ```bash
   pip install -r requirements.txt
   ```

4. **Variabel lingkungan** (opsional untuk deployed)
   Buat file `.env` di root proyek (tidak akan di‑commit karena sudah ada di `.gitignore`) atau set langsung di shell:
   ```bash
   export SECRET_KEY="your-super-secret-key"
   export ADMIN_USERNAME="admin"
   export ADMIN_PASSWORD="your-strong-password"
   export FLASK_APP=app.py
   export FLASK_ENV=development   # set to production for production
   ```

   Jika tidak diset, aplikasi akan menggunakan nilai default:
   - `SECRET_KEY` = `'hard to guess string'`
   - `ADMIN_USERNAME` = `'admin'`
   - `ADMIN_PASSWORD` = `'password'`

5. **Inisialisasi basis data**
   Aplikasi akan otomatis membuat tabel SQLite (`portfolio.db`) saat pertama kali dijalankan melalui `db.create_all()` dalam `app.py`. Jika ingin membuat ulang, hapus file `portfolio.db` dan jalankan kembali.

6. **Jalankan aplikasi**
   ```bash
   flask run
   # atau
   python app.py
   ```
   Buka browser ke `http://127.0.0.1:5000`.

## Penggunaan

- Akses halaman publik (`/`, `/about`, `/portfolio`, `/contact`) tanpa login.
- Untuk masuk ke dashboard admin, buka `http://127.0.0.1:5000/dashboard/login` dan masukkan username/password yang telah Anda set via environment variable (default: `admin` / `password`).
- Setelah login Anda dapat:
  - Menambah, mengedit, dan menghapus proyek (dengan unggah gambar thumbnail).
  - Mengedit profil pribadi (nama, headline, about, foto, dan daftar skill).
  - Melihat dan mengelola pesan masuk dari formulir kontak.

## Pengembangan & Testing

Untuk menjalankan uji coba sederhana (jika Anda menambahkan file uji nanti), Anda dapat menggunakan `pytest`:

```bash
pip install pytest
pytest
```

Saat ini proyek belum termasuk tes unit, tetapi struktur sudah siap untuk ditambahkan.

## Deployment (Produksi)

Berikut contoh pekerjaan untuk beberapa platform populer. Pastikan Anda mengatur `SECRET_KEY` dan kredensial admin yang aman di lingkungan produksi.

### Generic (Gunicorn)
```bash
gunicorn -w 4 -b 0.0.0.0:8000 "app:create_app()"
```

### Render
1. Buat layanan **Web Service**.
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `gunicorn -w 4 -b 0.0.0.0:$PORT "app:create_app()"`
4. Tambahkan Environment Variables sesuai bagian di atas.

### Railway
1. New Project → Deploy from Repo.
2. Pastikan buildpack Python terdeteksi.
3. Tambahkan variabel lingkungan di dashboard.
4. Railway secara otomatis menggunakan `gunicorn` jika ada `Procfile`; buat `Procfile` dengan isi:
   ```
   web: gunicorn -w 4 -b 0.0.0.0:$PORT "app:create_app()"
   ```

### PythonAnywhere
1. Unggah kode lewat tab **Files** atau clone repo.
2. Buat virtualenv di tab **Web** → mendaftarkan aplikasi Flask.
3. Pada file `wsgi.py` (yang otomatis dibuat) isi:
   ```python
   from app import create_app
   application = create_app()
   ```
4. Set environment variables di tab **Web** → **Environment variables**.
5. Reload web app.

### Catatan

### Kontribusi

Jika Anda menemukan bug atau memiliki fitur baru, silakan buat **issue** atau kirim **pull request**.

## Lisensi

Proyek ini dibuat untuk keperluan kelas **Pengantar Pemrograman**. Anda bebas menggunakan dan memodifikasinya untuk keperluan pembelajaran.

--- 

*Catatan:* Folder `static/uploads/` sengaja tidak masuk ke repository (lihat `.gitignore`). Saat pertama kali dijalankan, aplikasi akan membuat folder ini secara otomatis jika belum ada.

```