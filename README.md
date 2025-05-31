# Kelompok ABC
# SuperPower - Hand Tracking Effects

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.7+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/OpenCV-4.5+-green.svg" alt="OpenCV Version">
  <img src="https://img.shields.io/badge/MediaPipe-0.10+-orange.svg" alt="MediaPipe Version">
  <br>
  <b>Real-time hand tracking with interactive visual effects using Python, OpenCV, and MediaPipe</b>
</div>

## 📋 Tentang Proyek

Proyek Filter SuperPower adalah aplikasi berbasis Python yang dirancang untuk memberikan efek visual interaktif berupa ledakan partikel atau api yang mengikuti gerakan tangan pengguna. Aplikasi ini menggunakan teknologi MediaPipe untuk mendeteksi posisi dan gerakan tangan secara real-time, kemudian menambahkan efek visual dinamis yang muncul saat pengguna melakukan gestur tertentu seperti melambai atau menghentakkan tangan.

Proyek ini dikembangkan sebagai bagian dari tugas Ujian Akhir Semester mata kuliah IF4021-Sistem/Teknologi Multimedia pada program studi Teknik Informatika, yang diampu oleh Martin Clinton Tosima Manullang, S.T., M.T. ([@mctosima](https://github.com/mctosima)).

## ✨ Fitur Utama

- **Pelacakan Multi-Tangan**: Mendeteksi hingga 2 tangan sekaligus
- **Pengenalan Gestur**: Membedakan antara kepalan tangan, telapak tangan terbuka, dan jari telunjuk
- **Efek Visual Interaktif**:
  - Efek api yang mengikuti gerakan tangan
  - Jeak merah untuk gerakan jari
  - Ukuran efek yang menyesuaikan dengan jarak tangan dari kamera
- **Antarmuka Sederhana**: Mudah digunakan dengan kontrol gestur alami
- **Optimasi Kinerja**: Berjalan lancar di berbagai perangkat

## 🛠️ Teknologi

- **Python 3.7+** - Bahasa pemrograman utama
- **OpenCV** - Pemrosesan gambar dan video
- **MediaPipe** - Pelacakan tangan dan gestur
- **NumPy** - Komputasi numerik
- **imageio** - Pemrosesan file GIF

## 🚀 Panduan Instalasi

1. **Clone Repository**
   ```bash
   git clone https://github.com/username/SuperPower.git
   cd SuperPower
   ```

2. **Buat dan Aktifkan Virtual Environment**
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # macOS/Linux
   # source venv/bin/activate
   ```

3. **Instal Dependensi**
   ```bash
   pip install -r requirements.txt
   ```

## 🎮 Cara Menggunakan

1. Pastikan webcam terhubung dan berfungsi dengan baik
2. Jalankan program:
   ```bash
   python main.py
   ```
3. Kontrol Gestur:
   - **Telapak Tangan Terbuka**: Tampilkan efek api di tengah telapak tangan
   - **Jari Telunjuk**: Buat jejak merah mengikuti ujung jari
   - **Kepalan Tangan**: Reset pelacakan tangan
   - **ESC atau Q**: Keluar dari aplikasi

## 📁 Struktur Proyek

```
SuperPower/
├── effects/                  # Folder berisi efek GIF
│   └── efek-api-unscreen.gif  # Efek api default
├── main.py                   # Kode utama aplikasi
├── README.md                 # Dokumentasi
└── requirements.txt          # Dependensi proyek
```


# Anggota Tim
<img src="https://ik.imagekit.io/fliiaytbv/Cuplikan%20layar%202025-05-08%20111417.png?updatedAt=1746678657462" alt="Yani" width="40"/> | **Handayani** (122140166) | [@handayani](https://github.com/han5474ni) |
|------------------------------------|----------------------------------|--------------------------------------|
| ![francois](https://via.placeholder.com/60/FF0000/FFFFFF?text=Photo) | **Francois Novalentino Sinurat** (121140007) | [@Francois](https://github.com/FrancoisSinurat) |
| ![dimas](https://via.placeholder.com/60/CCCCCC/000000?text=Icon) | **Dimas Azi Rajab Aizar** (121140135) | [@Dimas](https://github.com/DimasAzi24) |

## Logbook Progress

| Minggu | Tanggal       | Progress |
|--------|---------------|----------|
| 1      | [24/04/2025]  | - Inisialisasi proyek |
| 2      | [25/04/2025]  | - Mencari Referensi Proyek |
| 3      | [02/05/2025]  | - Implementasi penuh program "SuperPower" menggunakan Python, OpenCV, dan MediaPipe. Fitur utama meliputi: deteksi tangan real-time, overlay efek api interaktif pada jari dan telapak tangan, UI tombol pemilihan filter efek video, serta rotasi dan masking efek agar terlihat dinamis. Telah dipush ke GitHub untuk dokumentasi dan kolaborasi. |
| 4      | [08/05/2025]  | - Penyusunan Template Laporan Akhir link: https://www.overleaf.com/7171988215mcwqvnjyscxm#abf677 |
| 5      | [21/05/2025]  | - Revisi kode |
| 6      | [30/05/2025]  | - Penyusunan Laporan |

## 📝 Laporan Akhir

Template laporan akhir dapat diakses di [Overleaf](https://www.overleaf.com/7171988215mcwqvnjyscxm#abf677).

---
<div align="center">
  Dibuat dengan ❤️ untuk IF4021 - Sistem/Teknologi Multimedia
</div>

