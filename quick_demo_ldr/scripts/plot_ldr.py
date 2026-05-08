#!/usr/bin/env python3
"""
Quick Demo Logger for LDR + LED PID Control
Usage: python scripts/plot_ldr.py --port COM3 (Windows) atau /dev/ttyUSB0 (Linux/Mac)
"""
import serial, argparse, csv, datetime, os
import matplotlib.pyplot as plt
import pandas as pd

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', required=True, help='Serial port')
    parser.add_argument('--baud', type=int, default=115200)
    parser.add_argument('--duration', type=int, default=60, help='Recording duration (seconds), 0 = infinite')
    parser.add_argument('--setpoint', type=float, default=2000.0, help='Expected setpoint ADC value')
    return parser.parse_args()

def main():
    args = parse_args()
    
    # Setup serial
    print(f"🔌 Connecting to {args.port} @ {args.baud}...")
    ser = serial.Serial(args.port, args.baud, timeout=1)
    print(f"✓ Connected!")
    
    # Prepare output
    os.makedirs('data', exist_ok=True)
    csv_path = f"data/ldr_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    data = []
    
    print(f"📝 Logging to {csv_path}")
    print("Format: time_ms,setpoint_adc,ldr_value,pwm_duty,error")
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
                
                # Skip non-data lines (headers, debug info)
                if not line or line.startswith('===') or line.startswith('Student') or \
                   line.startswith('Politeknik') or line.startswith('time_ms') or \
                   line.startswith('📊') or line.startswith('🔍'):
                    continue
                
                parts = line.split(',')
                if len(parts) == 5:
                    try:
                        row = {
                            'time_ms': int(parts[0]),
                            'setpoint': float(parts[1]),
                            'ldr_value': float(parts[2]),
                            'pwm': int(parts[3]),
                            'error': float(parts[4])
                        }
                        data.append(row)
                        print(f"\r📊 LDR: {row['ldr_value']:6.0f} | PWM: {row['pwm']:4d} | Err: {row['error']:+7.0f}", end='')
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
        print(f"\n💾 Saved {len(data)} samples to {csv_path}")
        
        # Plotting
        df = pd.DataFrame(data)
        df['time_sec'] = df['time_ms'] / 1000.0
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
        
        # Plot 1: LDR Value vs Time
        ax1.plot(df['time_sec'], df['ldr_value'], label='LDR Reading (ADC)', color='#2E86AB', linewidth=1.5)
        ax1.axhline(y=df['setpoint'].iloc[0], color='#A23B72', linestyle='--', label='Setpoint', linewidth=1)
        ax1.set_ylabel('ADC Value (0-4095)')
        ax1.legend(loc='upper right')
        ax1.grid(True, alpha=0.3)
        ax1.set_title('💡 Quick Demo: LDR + LED PID Control Response')
        
        # Plot 2: PWM & Error vs Time
        ax2_twin = ax2.twinx()
        ax2.plot(df['time_sec'], df['pwm'], label='PWM Duty', color='#F18F01', linewidth=1.5)
        ax2_twin.plot(df['time_sec'], df['error'], label='Error', color='#C73E1D', linestyle=':', linewidth=1)
        ax2.set_ylabel('PWM Duty (0-1023)', color='#F18F01')
        ax2_twin.set_ylabel('Error (ADC units)', color='#C73E1D')
        ax2.set_xlabel('Time (seconds)')
        ax2.grid(True, alpha=0.3)
        
        # Combine legends
        lines1, labels1 = ax2.get_legend_handles_labels()
        lines2, labels2 = ax2_twin.get_legend_handles_labels()
        ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
        
        plt.tight_layout()
        png_path = csv_path.replace('.csv', '.png')
        plt.savefig(png_path, dpi=150, bbox_inches='tight')
        print(f"📈 Plot saved as {png_path}")
        plt.show()
    else:
        print("⚠️  No data recorded. Check wiring & serial output.")

if __name__ == '__main__':
    main()
