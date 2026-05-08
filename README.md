# Campus-Project-Management-System

![GitHub repo size](https://img.shields.io/github/repo-size/username/Campus-Project-Management-System)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 📚 Deskripsi Repository

Repository ini berisi kumpulan **tugas dan proyek akademik** dari mahasiswa **Jurusan Teknik Elektro - Politeknik Negeri Malang (Polinema)**. Repository ini ditujukan untuk:

- 🎓 **Pembelajaran**: Dokumentasi materi sistem kendali, IoT, dan embedded systems
- 🔬 **Eksperimen**: Testing algoritma kontrol (PID, Fuzzy, dll) pada hardware
- 📖 **Dokumentasi**: Referensi untuk adik tingkat dan kolaborasi
- 📊 **Analisis**: Visualisasi data hasil eksperimen

---

## 👤 Identitas Mahasiswa

| Informasi | Detail |
|-----------|--------|
| **Nama** | [NAMA_LENGKAP_ANDA] |
| **NIM** | [NIM_ANDA] |
| **Kelas** | [KELAS_ANDA] |
| **Jurusan** | Teknik Elektro - Politeknik Negeri Malang |
| **Email** | [EMAIL_ANDA@student.polinema.ac.id](mailto:email) |
| **GitHub** | [@username](https://github.com/username) |

> ⚠️ **Catatan**: Ganti informasi di atas dengan data Anda sebelum commit.

---

## 📁 Daftar Proyek

### 1. 🌟 Light PID Control - BH1750 (Versi Final)
Implementasi **PID diskrit** untuk kontrol intensitas cahaya menggunakan sensor **BH1750** dan LED 12V.

| Fitur | Deskripsi |
|-------|-----------|
| **Sensor** | BH1750 (Digital I2C, 1-65535 lux) |
| **Aktuator** | LED 12V via MOSFET PWM |
| **Sampling Time** | 200ms |
| **Algoritma** | Discrete PID dengan anti-windup |
| **Analisis** | Python script untuk logging & plotting |

📂 **Lokasi**: [`light_pid_simple/`](light_pid_simple/)

```bash
cd light_pid_simple
pio run --target upload
python scripts/plot_lux.py --port /dev/ttyUSB0 --duration 60
```

📄 **File Penting**:
- `src/main.cpp` - Kode ESP32 dengan PID controller
- `scripts/plot_lux.py` - Real-time logger & plotter
- `MATERI_PRESENTASI.md` - Materi lengkap presentasi (diagram blok, analisis)
- `data/sample_data.csv` - Sample data eksperimen

---

### 2. ⚡ Quick Demo - LDR + LED 5V (Versi Cepat)
Versi **demo cepat** menggunakan **LDR analog** dan **LED 5V**. Cocok untuk testing di kelas tanpa komponen mahal.

| Fitur | Deskripsi |
|-------|-----------|
| **Sensor** | LDR + Voltage Divider (Analog ADC) |
| **Aktuator** | LED 5V dengan resistor 220Ω |
| **Sampling Time** | 200ms |
| **Algoritma** | Discrete PID (sama dengan versi BH1750) |
| **Harga** | < Rp 5.000,- |

📂 **Lokasi**: [`quick_demo_ldr/`](quick_demo_ldr/)

```bash
cd quick_demo_ldr
pio run --target upload
python scripts/plot_ldr.py --port /dev/ttyUSB0 --duration 60
```

📄 **File Penting**:
- `src/main.cpp` - Kode ESP32 dengan identitas mahasiswa
- `scripts/plot_ldr.py` - Logger khusus LDR
- `README.md` - Wiring diagram & tuning guide

---

## 📊 Perbandingan Kedua Proyek

| Aspek | BH1750 (Final) | LDR (Quick Demo) |
|-------|----------------|------------------|
| **Akurasi** | ±5% (kalibrasi pabrik) | ±20% (tergantung suhu) |
| **Output** | Lux (satuan nyata) | ADC value (0-4095) |
| **Interface** | I2C (digital) | Analog (ADC) |
| **Harga Sensor** | ~Rp 25.000 | ~Rp 2.000 |
| **Kompleksitas** | Sedang (butuh library) | Sangat sederhana |
| **Waktu Setup** | 15 menit | 5 menit |
| **Cocok Untuk** | Proyek final, laporan resmi | Demo kelas, quick test |

---

## 🧠 Materi Pembelajaran

Repository ini mencakup konsep-konsep berikut:

### 1. Sistem Kendali Diskrit
- ✅ PID controller dalam domain diskrit
- ✅ Sampling time & efeknya terhadap stabilitas
- ✅ Anti-windup integral
- ✅ Analisis respons step (rise time, settling time, overshoot)

### 2. Embedded Systems (ESP32)
- ✅ PWM generation dengan LEDC
- ✅ ADC reading & filtering
- ✅ I2C communication (BH1750)
- ✅ Serial communication untuk logging

### 3. Analisis Data dengan Python
- ✅ Real-time serial monitoring
- ✅ CSV data logging
- ✅ Plotting dengan matplotlib
- ✅ Statistical analysis dengan pandas

### 4. Dokumentasi Teknik
- ✅ Wiring diagram
- ✅ Block diagram sistem
- ✅ Transfer function & matematika kontrol
- ✅ Technical report writing

---

## 🚀 Quick Start

### Prerequisites
```bash
# Install Python dependencies
pip install pyserial matplotlib pandas

# Install PlatformIO (jika belum)
pip install platformio

# Atau via VS Code Extension: "PlatformIO IDE"
```

### Clone Repository
```bash
git clone https://github.com/username/Campus-Project-Management-System.git
cd Campus-Project-Management-System
```

### Pilih Proyek
```bash
# Versi Final (BH1750)
cd light_pid_simple

# ATAU Versi Quick Demo (LDR)
cd quick_demo_ldr
```

### Upload ke ESP32
```bash
pio run --target upload
pio device monitor
```

### Run Analysis
```bash
python scripts/plot_*.py --port /dev/ttyUSB0 --duration 60
```

---

## 📂 Struktur Repository

```
Campus-Project-Management-System/
├── README.md                   # 📘 Dokumen utama (file ini)
├── .gitignore                  # Ignore files
│
├── light_pid_simple/           # 🌟 PROYEK FINAL (BH1750)
│   ├── src/main.cpp            # PID controller + BH1750
│   ├── scripts/
│   │   ├── plot_lux.py         # Python logger
│   │   ├── test_with_sample_data.py
│   │   └── requirements.txt
│   ├── data/
│   │   ├── sample_data.csv     # Sample data
│   │   └── sample_output.png   # Sample grafik
│   ├── MATERI_PRESENTASI.md    # 📚 Materi presentasi lengkap
│   ├── platformio.ini
│   └── README.md
│
└── quick_demo_ldr/             # ⚡ QUICK DEMO (LDR)
    ├── src/main.cpp            # PID controller + LDR
    ├── scripts/
    │   ├── plot_ldr.py         # Python logger untuk LDR
    │   └── requirements.txt
    ├── data/                   # Output data eksperimen
    ├── platformio.ini
    └── README.md
```

---

## 📝 Log Aktivitas Repository

| Tanggal | Aktivitas | Deskripsi |
|---------|-----------|-----------|
| 2024-01-XX | 📦 Initial commit | Setup struktur repository |
| 2024-01-XX | ✨ Add BH1750 project | Implementasi PID dengan sensor BH1750 |
| 2024-01-XX | 📚 Add presentation material | Materi presentasi lengkap |
| 2024-01-XX | ⚡ Add LDR quick demo | Versi demo cepat dengan LDR |
| 2024-01-XX | 🔄 Update README | Penambahan identitas & dokumentasi |

---

## 🎯 Cara Menggunakan Repository Ini

### Untuk Mahasiswa
1. **Clone** repository ini
2. **Ganti identitas** di setiap `src/main.cpp`
3. **Pelajari** kode dan materi presentasi
4. **Test** dengan hardware (pilih versi sesuai kebutuhan)
5. **Analisis** hasil dengan Python script
6. **Dokumentasikan** hasil eksperimen Anda

### Untuk Dosen/Asisten
1. Review kode di `src/main.cpp` untuk verifikasi implementasi PID
2. Cek data CSV hasil eksperimen di folder `data/`
3. Evaluasi grafik respons sistem
4. Gunakan `MATERI_PRESENTASI.md` sebagai panduan penilaian

---

## ❓ FAQ

**Q: Mana yang harus saya gunakan, BH1750 atau LDR?**  
A: Gunakan **LDR** untuk demo cepat di kelas atau jika budget terbatas. Gunakan **BH1750** untuk proyek final dan laporan resmi karena akurasinya lebih tinggi.

**Q: Bagaimana cara tuning PID?**  
A: Lihat section "Tuning PID" di README masing-masing proyek. Mulai dengan Kp sedang, Ki kecil, Kd sedang. Naikkan Ki jika ada steady-state error, turunkan Kp jika osilasi.

**Q: Apakah bisa dijalankan di ESP8266?**  
A: Ya, dengan modifikasi minor. ESP8266 juga memiliki PWM dan ADC, tapi resolusi ADC hanya 10-bit (0-1023).

**Q: Bagaimana format pengumpulan tugas?**  
A: Kumpulkan:
- File `src/main.cpp` yang sudah diedit dengan identitas Anda
- Data CSV hasil eksperimen (minimal 60 detik recording)
- Grafik PNG hasil plotting
- Foto wiring/setup hardware
- Laporan singkat (max 3 halaman) analisis respons sistem

---

## 📞 Kontak

Jika ada pertanyaan, silakan hubungi:

- **Email**: [EMAIL_ANDA@student.polinema.ac.id](mailto:email)
- **GitHub Issues**: [Buka issue baru](https://github.com/username/Campus-Project-Management-System/issues)

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details.

---

**© 2024 - Politeknik Negeri Malang - Jurusan Teknik Elektro**

*"Knowledge grows when shared"* 🌱
