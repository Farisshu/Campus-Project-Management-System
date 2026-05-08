#!/usr/bin/env python3
"""
Light PID Logger & Plotter - Simple Version
Usage: python plot_lux.py --port COM3  (Windows) atau /dev/ttyUSB0 (Linux/Mac)
"""
import serial, argparse, csv, datetime, os
import matplotlib.pyplot as plt
import pandas as pd

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', required=True, help='Serial port')
    parser.add_argument('--baud', type=int, default=115200)
    parser.add_argument('--duration', type=int, default=300, help='Recording duration (seconds), 0 = infinite')
    return parser.parse_args()

def main():
    args = parse_args()
    
    # Setup serial
    ser = serial.Serial(args.port, args.baud, timeout=1)
    print(f"✓ Connected to {args.port} @ {args.baud}")
    
    # Prepare output
    os.makedirs('data', exist_ok=True)
    csv_path = f"data/report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    data = []
    
    print(f"📝 Logging to {csv_path}")
    print("Format: time_ms,setpoint_lux,actual_lux,pwm_duty,error")
    print("⏱️  Press Ctrl+C to stop recording and show plots\n")
    
    try:
        start_time = datetime.datetime.now()
        while True:
            # Check duration limit
            if args.duration > 0:
                elapsed = (datetime.datetime.now() - start_time).total_seconds()
                if elapsed >= args.duration:
                    print(f"\n⏱️  Duration reached ({args.duration}s), stopping...")
                    break
            
            # Read serial
            if ser.in_waiting:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                if line and not line.startswith('time_ms'):  # Skip header
                    parts = line.split(',')
                    if len(parts) == 5:
                        try:
                            row = {
                                'time_ms': int(parts[0]),
                                'setpoint': float(parts[1]),
                                'lux': float(parts[2]),
                                'pwm': int(parts[3]),
                                'error': float(parts[4])
                            }
                            data.append(row)
                            print(f"\r📊 Lux: {row['lux']:6.1f} | PWM: {row['pwm']:4d} | Err: {row['error']:+6.1f}", end='')
                        except ValueError:
                            pass
            
            # Small sleep to avoid CPU hog
            plt.pause(0.01)
            
    except KeyboardInterrupt:
        print("\n✋ Stopped by user")
    finally:
        ser.close()
    
    # Save to CSV
    if data:
        with open(csv_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        print(f"💾 Saved {len(data)} samples to {csv_path}")
        
        # Plotting
        df = pd.DataFrame(data)
        df['time_sec'] = df['time_ms'] / 1000.0
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
        
        # Plot 1: Lux vs Time
        ax1.plot(df['time_sec'], df['lux'], label='Actual Lux', color='#2E86AB', linewidth=1.5)
        ax1.axhline(y=df['setpoint'].iloc[0], color='#A23B72', linestyle='--', label='Setpoint', linewidth=1)
        ax1.set_ylabel('Illuminance (lux)')
        ax1.legend(loc='upper right')
        ax1.grid(True, alpha=0.3)
        ax1.set_title('🔆 Light Intensity PID Control Response')
        
        # Plot 2: PWM & Error vs Time
        ax2_twin = ax2.twinx()
        ax2.plot(df['time_sec'], df['pwm'], label='PWM Duty', color='#F18F01', linewidth=1.5)
        ax2_twin.plot(df['time_sec'], df['error'], label='Error', color='#C73E1D', linestyle=':', linewidth=1)
        ax2.set_ylabel('PWM Duty (0-1023)', color='#F18F01')
        ax2_twin.set_ylabel('Error (lux)', color='#C73E1D')
        ax2.set_xlabel('Time (seconds)')
        ax2.grid(True, alpha=0.3)
        
        # Combine legends
        lines1, labels1 = ax2.get_legend_handles_labels()
        lines2, labels2 = ax2_twin.get_legend_handles_labels()
        ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
        
        plt.tight_layout()
        plt.savefig(csv_path.replace('.csv', '.png'), dpi=150, bbox_inches='tight')
        print(f"📈 Plot saved as {csv_path.replace('.csv', '.png')}")
        plt.show()
    else:
        print("⚠️  No data recorded. Check wiring & serial output.")

if __name__ == '__main__':
    main()
