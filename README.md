# Web Portofolio Dinamis dengan Python Flask

Capstone project untuk mata kuliah Pengantar Pemrograman.

## Deskripsi

Aplikasi web portofolio pribadi dengan dashboard admin yang memproyek, profil, dan pesan masuk secara dinamisnis untuk mengelola konten proyek, profil, dan pesan masuk secara dinamis tanpa perlu mengubah kode program.

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
- **Upload gambar**: validasi tipe file (PNG/JPG/JPEG/GIF/WEBP) di sisi server, simpan ke static/uploads/, maksimal 5MB
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
├── static/
│   ├── css/
│   ├── js/
│   └── uploads/
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

## Setup dan Instalasi

1. Clone repository ini
2. Buat virtual environment (opsional disarankan):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Jalankan aplikasi:
   ```bash
   python app.py
   ```
5. Buka browser ke `http://localhost:5000`

## Penggunaan

- Halaman publik dapat diakses tanpa login.
- Untuk mengakses dashboard admin, buka `/dashboard/login` dan login dengan kredensial admin (akan dijelaskan nanti).
- Setelah login, Anda dapat mengelola proyek, profil, dan pesan melalui dashboard.

## Kontribusi

Jika Anda menemukan bug atau memiliki fitur baru, silakan buat issue atau pull request.

## Lisensi

Proyek ini dibuat untuk keperluan kelas Pengantar Pemrograman.

