# 🌟 Light Intensity PID Control System
## Tugas Kampus: Sistem Kendali Diskrit

Sistem kendali cahaya berbasis ESP32 dengan sensor BH1750 dan algoritma PID diskrit. Proyek ini mendemonstrasikan implementasi kontroler PID pada sistem embedded dengan analisis data menggunakan Python.

---

## 📋 Fitur Utama

- ✅ **PID Controller Diskrit** dengan sampling time 200ms
- ✅ **Anti-windup** untuk mencegah integral saturation
- ✅ **Sensor BH1750** (I2C) untuk pengukuran lux
- ✅ **PWM LED** sebagai aktuator (10-bit resolution)
- ✅ **Serial Logging** format CSV untuk analisis
- ✅ **Python Script** untuk visualisasi data real-time
- ✅ **Struktur Minimalis** - semua logika dalam 1 file

---

## 📁 Struktur Folder

```
light_pid_simple/
├── src/
│   └── main.cpp          # Kode utama: PID, sensor, PWM, logging
├── scripts/
│   ├── plot_lux.py       # Python: serial → CSV + grafik
│   └── requirements.txt  # Dependencies Python
├── data/
│   ├── report_*.csv      # Data hasil eksperimen
│   └── report_*.png      # Grafik visualisasi
├── platformio.ini        # Konfigurasi PlatformIO
├── README.md             # Dokumentasi ini
└── .gitignore
```

---

## 🔌 Wiring Diagram

### Komponen yang Dibutuhkan:
- ESP32 DevKit v1
- Sensor BH1750 (I2C)
- LED 12V + MOSFET (IRF540N) atau gunakan LED onboard GPIO 23
- Resistor 220Ω (untuk LED)

### Koneksi:

| BH1750 | ESP32 | Keterangan |
|--------|-------|------------|
| VCC    | 3.3V  | Power      |
| GND    | GND   | Ground     |
| SDA    | GPIO 21 | I2C Data |
| SCL    | GPIO 22 | I2C Clock |
| ADDR   | -     | Tidak terhubung (default 0x23) |

| LED/MOSFET | ESP32 | Keterangan |
|------------|-------|------------|
| Gate (MOSFET) | GPIO 23 | PWM Control |
| Source (MOSFET) | GND | Ground |
| Drain (MOSFET) | LED (-) | Load |
| LED (+) | 12V via Resistor | Power |

### Diagram Skematik:
```
         ┌─────────────┐
         │   ESP32     │
         │             │
    3.3V ├─┐       ┌───┤ GPIO 21 (SDA) ────┐
         │ │       │   │                   │
    GND  ├─┼───────┼───┤ GPIO 22 (SCL) ────┼─── BH1750
         │ │       │   │                   │
         │ └───────┘   │                   │
         │             │ GPIO 23 (PWM)     │
         │             └──────────┬────────┘
         │                        │
         │                    ┌───┴───┐
         │                    │ 10kΩ  │ (pulldown opsional)
         │                    └───┬───┘
         │                        │
         │                    Gate │
         │                    ┌────┴────┐
         │                    │ MOSFET  │
         │                    │ IRF540N │
         │              Source│         │Drain
         └────────────────────┤         ├──────────┐
                              │         │          │
                             GND        │        LED (-)
                                        │
                                       LED (+)
                                        │
                                       220Ω
                                        │
                                       12V
```

---

## 🚀 Cara Menggunakan

### 1️⃣ Install Dependencies

**PlatformIO (VS Code Extension):**
```bash
# Install PlatformIO Core (opsional, jika pakai CLI)
pip install platformio

# Atau install extension PlatformIO di VS Code
```

**Python Dependencies:**
```bash
cd scripts
pip install -r requirements.txt
```

### 2️⃣ Build & Upload Firmware

**Menggunakan VS Code + PlatformIO:**
1. Buka folder `light_pid_simple/` di VS Code
2. Klik tombol **✓ Build** (atau `Ctrl+Alt+B`)
3. Klik tombol **→ Upload** (atau `Ctrl+Alt+U`)

**Menggunakan PlatformIO CLI:**
```bash
cd light_pid_simple
pio run --target upload
```

### 3️⃣ Monitor Serial (Opsional)

**Via PlatformIO:**
```bash
pio device monitor
```

**Via Serial Monitor lain:**
- Baud rate: 115200
- Port: sesuaikan (COM3 di Windows, /dev/ttyUSB0 di Linux)

### 4️⃣ Jalankan Python Logger & Plotter

**Windows:**
```bash
python scripts/plot_lux.py --port COM3 --duration 60
```

**Linux/Mac:**
```bash
python3 scripts/plot_lux.py --port /dev/ttyUSB0 --duration 60
```

**Parameter:**
- `--port`: Port serial ESP32
- `--baud`: Baud rate (default: 115200)
- `--duration`: Durasi rekaman dalam detik (0 = infinite)

Output:
- `data/report_YYYYMMDD_HHMMSS.csv` - Data mentah
- `data/report_YYYYMMDD_HHMMSS.png` - Grafik visualisasi

---

## ⚙️ Konfigurasi PID

Edit bagian `CONFIG` di `src/main.cpp`:

```cpp
// PID Parameters
#define KP            8.0f    // Proportional gain
#define KI            0.05f   // Integral gain
#define KD            2.0f    // Derivative gain
#define SETPOINT_LUX  300.0f  // Target illuminance
#define SAMPLING_MS   200     // Sampling time (ms)
```

### 📊 Panduan Tuning PID

| Masalah | Solusi | Parameter |
|---------|--------|-----------|
| Respons lambat | Naikkan Kp | `KP += 1.0` |
| Error steady-state | Naikkan Ki sedikit | `KI += 0.02` |
| Osilasi/bergetar | Turunkan Kp atau naikkan Kd | `KP -= 1.0` atau `KD += 0.5` |
| Overshoot besar | Turunkan Ki atau naikkan Kd | `KI -= 0.01` atau `KD += 0.5` |

**Metode Tuning Manual:**
1. Set `KI = 0`, `KD = 0`
2. Naikkan `KP` sampai sistem mulai berosilasi
3. Turunkan `KP` sekitar 50% dari nilai osilasi
4. Tambahkan `KI` perlahan untuk menghilangkan error steady-state
5. Tambahkan `KD` untuk mengurangi overshoot

---

## 📈 Contoh Output

### Format Serial (CSV):
```csv
time_ms,setpoint_lux,actual_lux,pwm_duty,error
0,300.0,50.2,850,+249.8
200,300.0,120.5,720,+179.5
400,300.0,195.3,580,+104.7
600,300.0,250.8,420,+49.2
800,300.0,285.6,310,+14.4
1000,300.0,298.2,285,+1.8
```

### Grafik yang Dihasilkan:
- **Plot Atas**: Lux aktual vs setpoint vs waktu
- **Plot Bawah**: PWM duty cycle & error vs waktu

![Contoh Grafik](data/sample_output.png)

---

## 🔍 Analisis Sistem Kendali Diskrit

### Persamaan PID Diskrit:
```
u(k) = Kp·e(k) + Ki·Σe(k)·Δt + Kd·[e(k)-e(k-1)]/Δt
```

Dimana:
- `u(k)` = Output PWM pada sampling ke-k
- `e(k)` = Error (setpoint - measurement)
- `Δt` = Sampling time (0.2 detik)

### Spesifikasi Sistem:
- **Sampling Time**: 200 ms (5 Hz)
- **PWM Resolution**: 10-bit (0-1023)
- **PWM Frequency**: 5 kHz
- **Anti-windup**: ±500 (integral clamp)

---

## 🧪 Verifikasi & Testing

### Compile Test:
```bash
cd light_pid_simple
pio run
```

### Python Script Test (dengan sample data):
```bash
python scripts/plot_lux.py --port dummy --duration 0
```

---

## 📝 Catatan Penting

1. **Kalibrasi Sensor**: BH1750 mungkin perlu kalibrasi ulang jika pembacaan tidak akurat
2. **Ambient Light**: Tes di ruangan dengan cahaya terkontrol untuk hasil optimal
3. **PWM Frequency**: 5 kHz dipilih untuk menghindari flicker pada kamera
4. **Safety**: Pastikan MOSFET heatsink cukup untuk LED daya tinggi

---

## 🎯 Kriteria Penilaian

| Aspek | Bobot | File Bukti |
|-------|-------|------------|
| Implementasi PID | 30% | `src/main.cpp` |
| Akuisisi Data | 20% | `scripts/plot_lux.py` |
| Analisis & Visualisasi | 25% | `data/*.csv`, `data/*.png` |
| Dokumentasi | 15% | `README.md` |
| Testing & Validasi | 10% | CI/CD workflow |

---

## 📄 License

Proyek ini dibuat untuk tujuan edukasi (Tugas Kampus Sistem Kendali Diskrit).

---

## 👨‍💻 Kontributor

Dibuat dengan ❤️ untuk demonstrasi sistem kendali diskrit.
