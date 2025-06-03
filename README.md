<div align="center">
  <h1>✨ SuperPower - Hand Landmark Effects</h1>
  
  <p align="center">
    <img src="https://img.shields.io/badge/Python-3.7+-blue.svg" alt="Python Version">
    <img src="https://img.shields.io/badge/OpenCV-4.5+-green.svg" alt="OpenCV Version">
    <img src="https://img.shields.io/badge/MediaPipe-0.10+-orange.svg" alt="MediaPipe Version">
    <img src="https://img.shields.io/github/repo-size/han5474ni/Tugas_besar_Multimedia" alt="Repo Size">
  </p>
  
  <p><b>Real-time hand landmark with interactive visual effects Superpower using Python, OpenCV, and MediaPipe</b></p>
  
  [Demo Video](#-Demo) •
  [Fitur](#-fitur-utama) •
  [Instalasi](#-panduan-instalasi) •
  [Cara Menggunakan](#-cara-menggunakan)
</div>

## 📋 Tentang Proyek

![Demo GIF](https://raw.githubusercontent.com/han5474ni/Tugas_besar_MultiMedia/main/effects/efek-api-unscreen.gif)

Proyek Filter SuperPower adalah filter Augmented Reality (AR) yang menggunakan MediaPipe dan OpenCV untuk mendeteksi gerakan tangan secara real-time dan menambahkan efek visual interaktif berupa animasi api yang mengikuti gesture pengguna. 

### 🔥 Fitur Unggulan
- **Multi-Hand Tracking** - Dukung hingga 2 tangan sekaligus
- **Gesture Recognition** - Deteksi kepalan, telapak terbuka, dan jari telunjuk
- **Efek Visual Dinamis** - Animasi api yang responsif mengikuti gerakan
- **Optimasi Real-time** - Performa lancar dengan algoritma smoothing
- **User-friendly** - Kontrol intuitif dengan gestur alami

Dikembangkan sebagai bagian dari tugas Ujian Akhir Semester mata kuliah IF4021-Sistem/Teknologi Multimedia pada program studi Teknik Informatika, yang diampu oleh Martin Clinton Tosima Manullang, S.T., M.T. ([@mctosima](https://github.com/mctosima)).

## ✨ Fitur Utama

### 🖐️ Deteksi & Pelacakan
- Mendeteksi hingga 2 tangan sekaligus
- Pelacakan landmark tangan 21 titik
- Responsif dengan gerakan cepat

### ✨ Efek Visual
- **Efek Api Dinamis** - Mengikuti kontur tangan
- **Jejak Merah** - Garis mengalir di belakang jari
- **Bayangan & Glow** - Kedalaman visual yang menarik
- **Transisi Halus** - Perubahan efek yang natural

### ⚡ Performa
- Optimasi real-time
- Penggunaan CPU yang efisien
- Kompatibel dengan berbagai perangkat

### 🎮 Kontrol Intuitif
- **Telapak Terbuka** - Aktifkan efek api besar
- **Jari Telunjuk** - Aktifkan jejak merah
- **Kepalan Tangan** - Reset efek
- **ESC/Q** - Keluar aplikasi

## 🛠️ Teknologi

- **Python 3.7+** - Bahasa pemrograman utama
- **OpenCV** - Pemrosesan gambar dan video
- **MediaPipe** - Pelacakan tangan dan gestur
- **NumPy** - Komputasi numerik
- **imageio** - Pemrosesan file GIF

## 🚀 Panduan Instalasi

1. **Clone Repository**
   ```bash
   git clone https://github.com/han5474ni/Tugas_besar_Multimedia.git
   cd Tugas_besar_Multimedia
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
| <img src="https://ik.imagekit.io/fliiaytbv/Cuplikan%20layar%202025-05-08%20111417.png?updatedAt=1746678657462" width="40"/> | **Handayani** (122140166) | [@handayani](https://github.com/han5474ni) |
|------------------------------------|----------------------------------|--------------------------------------|
| <img src="https://github.com/user-attachments/assets/e6e42d96-1efe-4c66-89ae-a4e16cb57a2e" width="40"/> | **Francois Novalentino Sinurat** (121140007) | [@Francois](https://github.com/FrancoisSinurat) |
| <img src="https://github.com/user-attachments/assets/f9e81343-d8f8-4783-96e3-c316d81795c5" width="40"/> | **Dimas Azi Rajab Aizar** (121140135) | [@Dimas](https://github.com/DimasAzi24) |


## 📅 Logbook Progress

<details>
<summary>Lihat Riwayat Perkembangan Proyek</summary>

| Minggu | Tanggal       | Progress |
|--------|---------------|----------|
| 1 | 24/04/2025 | • Inisialisasi proyek<br>• Penyusunan rencana pengembangan |
| 2 | 25/04/2025 | • Riset teknologi<br>• Pengumpulan referensi proyek serupa <br>• https://vt.tiktok.com/ZSrvavKEX/ |
| 3 | 02/05/2025 | • Implementasi deteksi tangan real-time<br>• Integrasi efek api dasar<br>• Pembuatan UI kontrol |
| 4 | 08/05/2025 | • Pembuatan template laporan<br>• Dokumentasi kode |
| 5 | 21/05/2025 | • Optimasi kode<br>• Perbaikan bug |
| 6 | 30/05/2025 | • Penyusunan laporan<br>• Pengujian performa |
| 7 | 31/05/2025 | • Implementasi Finger Trail System<br>• Finalisasi laporan |

</details>

## 🎥 Demo

[![Tonton Demo 1](https://img.youtube.com/vi/OW3rP_mNTUo/0.jpg)](https://youtu.be/OW3rP_mNTUo)
[![Tonton Demo 2](https://img.youtube.com/vi/MoOCuSg1Aos/0.jpg)](https://youtu.be/MoOCuSg1Aos?si=25CbY0WtLoxxRG-c)

## 🙏 Ucapan Terima Kasih

- Dosen pengampu: Martin Clinton Tosima Manullang, S.T., M.T.
- Rekan-rekan kelompok yang telah berkontribusi

---

<div align="center">
  Dibuat dengan ❤️ untuk Tugas Besar Mata Kuliah Multimedia
</div>
