/**
 * Light Intensity PID Control - Single File Version
 * Tugas: Sistem Kendali Diskrit
 * MCU: ESP32 | Sensor: BH1750 | Actuator: LED PWM
 * Output Serial: timestamp,setpoint,lux,pwm,error
 */

#include <Arduino.h>
#include <Wire.h>
#include <BH1750.h>

// ========== CONFIG ==========
#define LED_PIN       23      // PWM pin ke MOSFET/LED
#define SDA_PIN       21
#define SCL_PIN       22
#define SAMPLING_MS   200     // Sampling time PID (ms)
#define PWM_RES       10      // 10-bit = 0-1023
#define PWM_FREQ      5000    // 5kHz PWM frequency

// PID Parameters (start conservative)
#define KP            8.0f
#define KI            0.05f
#define KD            2.0f
#define SETPOINT_LUX  300.0f  // Target kenyamanan
#define PWM_MIN       0
#define PWM_MAX       1023
#define INTEGRAL_MAX  500.0f  // Anti-windup limit

// ========== GLOBALS ==========
BH1750 lightSensor;
unsigned long lastSample = 0;
float error_prev = 0, integral = 0;
int pwm_output = 0;

// ========== PID COMPUTE (Discrete) ==========
float pid_compute(float setpoint, float measurement) {
  float error = setpoint - measurement;
  integral += error * (SAMPLING_MS / 1000.0);
  
  // Anti-windup
  if (integral > INTEGRAL_MAX) integral = INTEGRAL_MAX;
  if (integral < -INTEGRAL_MAX) integral = -INTEGRAL_MAX;
  
  float derivative = (error - error_prev) / (SAMPLING_MS / 1000.0);
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
  Wire.begin(SDA_PIN, SCL_PIN);
  
  // LED PWM setup (ESP32 LEDC)
  ledcSetup(0, PWM_FREQ, PWM_RES);  // channel 0
  ledcAttachPin(LED_PIN, 0);
  ledcWrite(0, 0);
  
  // BH1750 init
  if (!lightSensor.begin(BH1750::CONTINUOUS_HIGH_RES_MODE, 0x23, &Wire)) {
    Serial.println("❌ BH1750 not detected!");
    while(1) delay(100);
  }
  lightSensor.calibrateTiming();
  
  delay(100);
  Serial.println("time_ms,setpoint_lux,actual_lux,pwm_duty,error"); // CSV header
}

// ========== LOOP ==========
void loop() {
  unsigned long now = millis();
  
  // Sampling time enforcement
  if (now - lastSample < SAMPLING_MS) return;
  lastSample = now;
  
  // Read sensor
  float lux = lightSensor.readLightLevel();
  if (isnan(lux) || lux < 0) lux = 0;
  
  // PID compute
  pwm_output = (int)pid_compute(SETPOINT_LUX, lux);
  ledcWrite(0, pwm_output);  // Apply PWM
  
  // Compute error for logging
  float error = SETPOINT_LUX - lux;
  
  // Serial output (CSV format for Python parser)
  Serial.printf("%lu,%.1f,%.1f,%d,%.1f\n", 
                now, SETPOINT_LUX, lux, pwm_output, error);
  
  // Optional: debug to Serial Monitor (uncomment if needed)
  // Serial.printf("Lux: %.1f | PWM: %d | Err: %.1f\n", lux, pwm_output, error);
}
