# Quick Demo: LDR + LED 5V PID Control

## 🎯 Deskripsi
Versi demo cepat untuk tugas Sistem Kendali Diskrit menggunakan **LDR (Light Dependent Resistor)** dan **LED 5V** sebagai alternatif dari BH1750. Cocok untuk testing cepat dan demonstrasi di kelas.

## 👤 Identitas Mahasiswa
```
Nama: [NAMA_ANDA]
NIM: [NIM_ANDA]
Kelas: [KELAS_ANDA]
Jurusan: Teknik Elektro - Politeknik Negeri Malang
Mata Kuliah: Sistem Kendali Diskrit
Dosen Pengampu: [NAMA_DOSEN]
```

## 🔌 Wiring Diagram (Sangat Sederhana)

### Komponen yang Dibutuhkan:
- ESP32 DevKit
- LDR (Photoresistor)
- Resistor 10kΩ (untuk voltage divider LDR)
- LED 5V (atau LED putih biasa)
- Resistor 220Ω (untuk LED)
- Kabel jumper

### Skema Wiring:

```
     +3.3V ──────┬───────────────+
                 │               │
                [LDR]           [10kΩ]
                 │               │
                 ├──────→ GPIO34 │
                 │    (VP/ADC)   │
                GND             GND

     GPIO23 ───[220Ω]───[LED]─── GND
     (PWM)              (+)
```

### Detail Koneksi:

| Komponen | Pin 1 | Pin 2 | Keterangan |
|----------|-------|-------|------------|
| **LDR** | +3.3V | GPIO34 | Voltage divider atas |
| **Resistor 10k** | GPIO34 | GND | Voltage divider bawah |
| **LED** | GPIO23 (via 220Ω) | GND | Anoda ke PWM, Katoda ke GND |
| **Resistor 220Ω** | GPIO23 | LED (+) | Current limiter |

### Foto Wiring (Referensi):
```
        ESP32
    ┌─────────────┐
    │             │
    │  GPIO34 ────┼───┬───[LDR]─── +3.3V
    │   (VP/ADC)  │   │
    │             │   └───[10k]─── GND
    │             │
    │  GPIO23 ────┼───[220Ω]───[LED]─── GND
    │   (PWM)     │
    │             │
    └─────────────┘
```

## ⚙️ Parameter PID Default

```cpp
#define KP            15.0f   // Proportional gain
#define KI            0.08f   // Integral gain
#define KD            3.0f    // Derivative gain
#define SETPOINT_ADC  2000.0f // Target ADC value (sesuaikan!)
#define SAMPLING_MS   200     // Sampling time 200ms
```

### Cara Menentukan Setpoint:
1. Upload code tanpa feedback (PWM fixed)
2. Baca nilai LDR di Serial Monitor
3. Pilih nilai antara 1000-3000 (tergantung cahaya ruangan)
4. Update `SETPOINT_ADC` di `src/main.cpp`

## 🚀 Cara Menggunakan

### 1. Install Dependencies Python
```bash
cd quick_demo_ldr
pip install -r scripts/requirements.txt
```

### 2. Edit Identitas Mahasiswa
Buka `src/main.cpp` dan ganti:
```cpp
// Ganti ini:
Student: [NAMA_ANDA] | NIM: [NIM_ANDA]

// Menjadi data Anda:
Student: Ahmad Rizky | NIM: 2041720123
```

### 3. Upload ke ESP32
```bash
# Dengan PlatformIO
pio run --target upload

# Atau via Arduino IDE
# - Buka src/main.cpp
# - Pilih board: ESP32 Dev Module
# - Upload
```

### 4. Monitoring & Logging
```bash
# Windows (ganti COM3 dengan port Anda)
python scripts/plot_ldr.py --port COM3 --duration 60

# Linux/Mac
python scripts/plot_ldr.py --port /dev/ttyUSB0 --duration 60
```

### 5. Tuning PID (Jika Perlu)

| Gejala | Solusi |
|--------|--------|
| Respons lambat, error menetap | ↑ Ki (misal: 0.10) |
| Osilasi/bergetar | ↓ Kp atau ↑ Kd |
| Overshoot besar | ↓ Kp, ↑ Kd |
| Steady-state error | ↑ Ki sedikit |

## 📊 Output Data

Format CSV: `time_ms,setpoint_adc,ldr_value,pwm_duty,error`

Contoh output:
```csv
time_ms,setpoint_adc,ldr_value,pwm_duty,error
200,2000.0,450.0,1023,+1550.0
400,2000.0,980.0,1023,+1020.0
600,2000.0,1450.0,856,+550.0
...
```

## 📈 Analisis Hasil

Setelah running, akan dihasilkan:
- `data/ldr_report_YYYYMMDD_HHMMSS.csv` - Data mentah
- `data/ldr_report_YYYYMMDD_HHMMSS.png` - Grafik respons

### Metrik Kinerja:
- **Rise Time**: Waktu dari 10% → 90% setpoint
- **Settling Time**: Waktu hingga stabil ±5% setpoint
- **Overshoot**: Persentase kelebihan dari setpoint
- **Steady-State Error**: Error residual setelah stabil

## 🔍 Troubleshooting

| Masalah | Solusi |
|---------|--------|
| Nilai LDR selalu 0 | Cek wiring voltage divider |
| LED tidak menyala | Cek polaritas LED & resistor |
| Data tidak muncul di serial | Cek baudrate (115200) |
| Osilasi parah | Turunkan Kp jadi 10.0, naikkan Kd jadi 5.0 |
| Respons terlalu lambat | Naikkan Ki jadi 0.12 |

## 📝 Perbedaan dengan Versi BH1750

| Aspek | LDR (Quick Demo) | BH1750 |
|-------|------------------|--------|
| Sensor | Analog (ADC) | Digital (I2C) |
| Akurasi | ±20% | ±5% |
| Harga | Sangat murah (~Rp 2k) | Lebih mahal (~Rp 25k) |
| Wiring | Simpel (3 kabel) | Sedang (4 kabel) |
| Library | Tidak perlu | Butuh BH1750.h |
| Satuan | ADC value (0-4095) | Lux (nyata) |
| Cocok untuk | Demo cepat, belajar | Proyek final, akurasi tinggi |

## ✅ Checklist Pengumpulan

- [ ] Edit identitas di `src/main.cpp`
- [ ] Test hardware (LDR + LED)
- [ ] Running minimal 60 detik
- [ ] Generate grafik PNG
- [ ] Simpan CSV hasil eksperimen
- [ ] Dokumentasi foto wiring
- [ ] Analisis respons sistem

---

**© 2024 - Politeknik Negeri Malang - Teknik Elektro**
