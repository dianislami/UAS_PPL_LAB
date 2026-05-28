# 🪙 CRYPTEXA - Cryptocurrency Portfolio Platform

CRYPTEXA adalah platform modern pemantau portofolio cryptocurrency futuristik yang dirancang dengan antarmuka bertema dark-cyberpunk yang elegan dan responsif. Pengguna dapat melacak harga koin cryptocurrency terupdate secara real-time, mencatat riwayat transaksi beli (BUY) secara instan ke dalam database, melihat analisis performa portofolio lanjutan, serta mengelola koin yang tersedia langsung melalui Dashboard Admin khusus.

Aplikasi ini menggunakan kombinasi arsitektur **Django (Python)** sebagai core backend engine-nya dan antarmuka dengan sentuhan **Tailwind CSS** modern untuk memastikan performa yang cepat, aman, dan modern.

---

## Fitur Utama

1. **Futuristic Cryptography Trackers**  
   Tampilan daftar koin cryptocurrency dengan informasi peringkat, simbol koin, harga langsung, serta persentase perubahan harga yang dinamis dan terstandarisasi.
   
2. **Instant & Secure Transaction Database-Sync**  
   Setiap transaksi beli (BUY) yang dilakukan oleh pengguna langsung tersinkronisasi dan disimpan secara permanen ke dalam database SQLite, mengeleminasi hilangnya data sesi di server.

3. **Advanced Portfolio Intelligence & Metrics**  
   Dashboard portofolio investor lengkap dengan metrik kalkulasi tingkat profesional, meliputi:
   * **Total Valuation & Total P&L**: Valuasi portofolio terupdate real-time berbasis harga koin terkini.
   * **Diversifikasi Aset**: Persentase kepemilikan koin.
   * **Best Asset & Worst Asset**: Penentuan aset dengan tingkat kepemilikan paling menguntungkan (Highest Profit) dan yang sedang kurang menguntungkan secara otomatis.
   * **Graph allocation**: Representasi visual pertumbuhan aset.

4. **Dedicated Admin Control Panel**  
   Ruang kendali khusus bagi administrator untuk:
   * Menambahkan koin/aset crypto baru ke dalam ekosistem.
   * Melakukan pembaruan harga (*Price updates*), penyesuaian peringkat koin (*Global Rank*), atau deskripsi koin secara instan.
   * Menghapus aset koin dari sistem.

---

## Teknologi & Arsitektur yang Digunakan

Aplikasi ini dirancang dengan struktur monolitik modern yang kokoh dan mudah deployable:

* **Backend Engine / Model-View-Template**: [Django 5.x Framework](https://www.djangoproject.com/) (Python 3)  
* **Database**: **SQLite** (menggunakan Django ORM relasional untuk mencatat relasi koin, transaksi, akun portofolio, dan user)  
* **UI & Styling**: **Tailwind CSS v4** dengan penyesuaian custom themes elegan (*Futuristic Slate Grays*, *Luminous Cyan Glows*, *Clean Typography*)  
* **Interactive Charts**: Responsive interactive chart rendering bawaan.

---

## Struktur Folder Aplikasi

Berikut adalah gambaran arsitektur folder utama Cryptexa:

```text
├── core/                  # Aplikasi utama Django (home landing page, auth, base config)
├── coins/                 # Modul Django untuk daftar koin, detail statistik, & feed koin
├── portfolio/             # Modul transaksi, portofolio engine, & metrik analitik finansial
├── dashboard/             # Modul admin panel untuk insert/update/delete koin
├── templates/             # Folder template HTML global dengan desain visual premium Tailwind
│   ├── base.html          # Shell layout utama dengan header/footer & styling global
│   ├── core/              # Template landing page & login form
│   ├── coins/             # Template daftar koin explorer & detail transaksi
│   ├── portfolio/         # Template dashboard kalkulasi portofolio
│   └── dashboard/         # Template form manajemen admin & edit koin
├── cryptexa/              # Konfigurasi sistem Django induk (settings.py, urls.py, wsgi.py)
├── db.sqlite3             # Database lokal SQLite tempat semua transaksi & koin tersimpan
├── manage.py              # Entry-point standard Django command-line utility
└── README.md              # File panduan informasi dan setup aplikasi
```

---

## Panduan Cara Menjalankan Aplikasi di Komputer Lokal

#### Langkah 1: Clone Repository
Buka terminal dan lakukan clone proyek:
```bash
git clone <URL_REPOSITORY_GITHUB_ANDA>
cd cryptexa
```

#### Langkah 2: Buat & Aktifkan Virtual Environment **(Opsional)**
* Untuk **macOS/Linux**:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
* Untuk **Windows (Command Prompt / Powershell)**:
  ```cmd
  python -m venv venv
  venv\Scripts\activate
  ```

#### Langkah 3: Install Dependensi Django (Python)
```bash
pip install django
```

#### Langkah 4: Migrasikan Database SQLite Lokal
Migrasikan schema tabel database untuk koin, transaksi, portofolio, dan auth bawaan Django:
```bash
python manage.py makemigrations core coins portfolio dashboard
python manage.py migrate
```

#### Langkah 5: Jalankan Server Lokal Django
```bash
python manage.py runserver
```
Buka browser favorit Anda dan akses alamat:
**[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## Pengaturan Default Akun Admin
Jika Anda ingin masuk ke admin panel (/dashboard/) untuk mendemokan edit data koin secara lokal melalui Django Admin atau custom Dashboard Admin:
* Akun superuser default akan otomatis dibuat oleh sistem jika sistem mendeteksi tidak ada user:
  * **Username**: `admin`
  * **Password**: `admin123`

Untuk membuat superuser tambahan secara manual melalui terminal lokal:
```bash
python manage.py createsuperuser
```

---

*Selamat menggunakan **CRYPTEXA**! Kelola dan kalkulasikan portofolio aset kripto Anda secara aman dan tanpa hambatan dengan performa real-time.*
