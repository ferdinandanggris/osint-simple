```markdown
# 🕵️‍♂️ OSINT-SIMPLE

**Simple Open Source Intelligence Tool** berbasis Web (Flask) untuk investigasi akademik dan visual secara otomatis.

Tools ini menggabungkan teknik scraping API dan Browser Automation (Selenium) untuk mengumpulkan informasi publik yang tersebar (PDDIKTI & Google Lens) ke dalam satu dashboard terintegrasi.

## 🚀 Fitur Utama

### 1. Academic Intelligence (PDDIKTI Hunter)
* **API Decryption:** Melakukan dekripsi payload AES-256 dari API publik PDDIKTI untuk mendapatkan data mentah.
* **Deep Search:** Mencari data Mahasiswa (NIM, Prodi, Status) dan Dosen (NIDN, Riwayat Mengajar).
* **Bypass:** Menggunakan header spoofing untuk menghindari deteksi bot sederhana.

### 2. Visual Intelligence (Lens Scraper)
* **Reverse Image Search:** Menggunakan Google Lens untuk mencari sumber gambar, lokasi, atau identitas visual.
* **Auto-Upload:** Mendukung upload file lokal yang otomatis diinjeksikan ke Google Images via Selenium.
* **Result Scraping:** Mengambil judul, link sumber, dan thumbnail dari hasil pencarian visual.

---

## 🛠️ Technical Stack

* **Backend:** Python 3.10+, Flask
* **Frontend:** HTML5, Bootstrap 5, jQuery
* **Automation:** Selenium WebDriver (Chrome)
* **Cryptography:** PyCryptodome (AES-CBC)
* **Networking:** Requests

---

## ⚙️ Instalasi

1.  **Clone Repository**
    ```bash
    git clone [https://github.com/username-anda/osint-simple.git](https://github.com/username-anda/osint-simple.git)
    cd osint-simple
    ```

2.  **Buat Virtual Environment**
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # Linux/Mac
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Jalankan Aplikasi**
    ```bash
    python app.py
    ```
    Buka browser dan akses: `http://127.0.0.1:5000`

---

## 📂 Struktur Project


```

osint-simple/
├── app.py              # Main Flask Controller
├── pddikti_lib.py      # Modul Decryptor & API Wrapper PDDIKTI
├── lens_lib.py         # Modul Selenium Automation Google Lens
├── requirements.txt    # Daftar Library
├── static/
│   └── uploads/        # Temp storage untuk upload gambar
└── templates/
└── index.html      # Dashboard UI

```

---

## ⚠️ Disclaimer

**EDUCATIONAL PURPOSE ONLY.**
Alat ini dibuat untuk tujuan edukasi dan riset keamanan siber (OSINT). Pengembang tidak bertanggung jawab atas penyalahgunaan informasi yang didapatkan melalui alat ini. Gunakan dengan bijak dan etis.

```

---
