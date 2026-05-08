/**
 * Quick Demo: LDR + LED 5V PID Control
 * Tugas: Sistem Kendali Diskrit - Versi Demo Cepat
 * MCU: ESP32 | Sensor: LDR (Analog) | Actuator: LED 5V via PWM
 * 
 * Identitas Mahasiswa:
 * Nama: [NAMA_ANDA]
 * NIM: [NIM_ANDA]
 * Kelas: [KELAS_ANDA]
 * Jurusan: Teknik Elektro - Politeknik Negeri Malang
 * 
 * Wiring Sederhana:
 * - LDR + Resistor 10k (voltage divider) → GPIO34 (VP)
 * - LED 5V + Resistor 220Ω → GPIO23 (PWM)
 * 
 * Output Serial: timestamp,setpoint,ldr_value,pwm_duty,error
 */

#include <Arduino.h>

// ========== CONFIG ==========
#define LDR_PIN       34      // Analog pin untuk LDR (GPIO34 = VP)
#define LED_PIN       23      // PWM pin untuk LED 5V
#define SAMPLING_MS   200     // Sampling time PID (ms)
#define PWM_RES       10      // 10-bit = 0-1023
#define PWM_FREQ      5000    // 5kHz PWM frequency
#define ADC_ATTEN     ADC_11DB // 0-3.3V range

// PID Parameters (tuned untuk LDR)
#define KP            15.0f
#define KI            0.08f
#define KD            3.0f
#define SETPOINT_ADC  2000.0f // Target nilai ADC (sesuaikan dengan cahaya ruang)
#define PWM_MIN       0
#define PWM_MAX       1023
#define INTEGRAL_MAX  800.0f  // Anti-windup limit

// ========== GLOBALS ==========
unsigned long lastSample = 0;
float error_prev = 0, integral = 0;
int pwm_output = 0;

// ========== READ LDR (Smoothed) ==========
float read_ldr() {
  const int samples = 5;
  long sum = 0;
  for (int i = 0; i < samples; i++) {
    sum += analogRead(LDR_PIN);
    delay(2);
  }
  return (float)sum / samples;
}

// ========== PID COMPUTE (Discrete) ==========
float pid_compute(float setpoint, float measurement) {
  float error = setpoint - measurement;
  
  // Integral with anti-windup
  integral += error * (SAMPLING_MS / 1000.0);
  if (integral > INTEGRAL_MAX) integral = INTEGRAL_MAX;
  if (integral < -INTEGRAL_MAX) integral = -INTEGRAL_MAX;
  
  // Derivative
  float derivative = (error - error_prev) / (SAMPLING_MS / 1000.0);
  
  // PID output
  float output = KP * error + KI * integral + KD * derivative;
  
  // Clamp output
  if (output < PWM_MIN) output = PWM_MIN;
  if (output > PWM_MAX) output = PWM_MAX;
  
  error_prev = error;
  return output;
}

// ========== SETUP ==========
void setup() {
  Serial.begin(115200);
  
  // ADC configuration for LDR
  analogReadResolution(12);  // 12-bit ADC (0-4095)
  analogSetAttenuation(ADC_ATTEN);
  
  // LED PWM setup (ESP32 LEDC)
  ledcSetup(0, PWM_FREQ, PWM_RES);  // channel 0
  ledcAttachPin(LED_PIN, 0);
  ledcWrite(0, 0);
  
  // Warm-up delay
  delay(500);
  
  // Print identity header
  Serial.println("=== QUICK DEMO: LDR + LED PID CONTROL ===");
  Serial.println("Student: [NAMA_ANDA] | NIM: [NIM_ANDA]");
  Serial.println("Politeknik Negeri Malang - Electronics Engineering");
  Serial.println("===========================================");
  Serial.println("time_ms,setpoint_adc,ldr_value,pwm_duty,error"); // CSV header
  
  // Initial reading
  float initial_ldr = read_ldr();
  Serial.printf("📊 Initial LDR value: %.0f (Target: %.0f)\n", initial_ldr, SETPOINT_ADC);
}

// ========== LOOP ==========
void loop() {
  unsigned long now = millis();
  
  // Sampling time enforcement
  if (now - lastSample < SAMPLING_MS) return;
  lastSample = now;
  
  // Read LDR sensor
  float ldr_value = read_ldr();
  
  // PID compute
  pwm_output = (int)pid_compute(SETPOINT_ADC, ldr_value);
  ledcWrite(0, pwm_output);  // Apply PWM to LED
  
  // Compute error for logging
  float error = SETPOINT_ADC - ldr_value;
  
  // Serial output (CSV format for Python parser)
  Serial.printf("%lu,%.1f,%.1f,%d,%.1f\n", 
                now, SETPOINT_ADC, ldr_value, pwm_output, error);
  
  // Optional: Debug every 10 samples
  static int counter = 0;
  if (++counter % 10 == 0) {
    Serial.printf("🔍 Debug: LDR=%.0f | PWM=%d | Err=%.1f\n", ldr_value, pwm_output, error);
  }
}
