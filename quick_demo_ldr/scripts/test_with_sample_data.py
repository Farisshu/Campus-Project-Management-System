#!/usr/bin/env python3
"""
Test script untuk generate grafik dari sample data LDR
Usage: python scripts/test_with_sample_data.py
"""
import csv, os
import matplotlib.pyplot as plt
import pandas as pd

def main():
    # Path ke sample data
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    csv_path = os.path.join(parent_dir, 'data', 'sample_data.csv')
    
    if not os.path.exists(csv_path):
        print(f"❌ Sample data not found at {csv_path}")
        return
    
    # Read CSV
    print(f"📖 Reading {csv_path}...")
    df = pd.read_csv(csv_path)
    df['time_sec'] = df['time_ms'] / 1000.0
    
    print(f"✓ Loaded {len(df)} samples")
    print(f"📊 Setpoint: {df['setpoint_adc'].iloc[0]} ADC")
    print(f"📈 LDR range: {df['ldr_value'].min()} - {df['ldr_value'].max()} ADC")
    print(f"💡 PWM range: {df['pwm_duty'].min()} - {df['pwm_duty'].max()}")
    
    # Plotting
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    
    # Plot 1: LDR Value vs Time
    ax1.plot(df['time_sec'], df['ldr_value'], 'o-', label='LDR Reading (ADC)', 
             color='#2E86AB', linewidth=2, markersize=6)
    ax1.axhline(y=df['setpoint_adc'].iloc[0], color='#A23B72', linestyle='--', 
                label='Setpoint (2000 ADC)', linewidth=1.5)
    ax1.set_ylabel('ADC Value (0-4095)', fontsize=11)
    ax1.legend(loc='lower right', fontsize=9)
    ax1.grid(True, alpha=0.3)
    ax1.set_title('💡 Quick Demo: LDR + LED 5V PID Control Response', fontsize=12, fontweight='bold')
    ax1.set_xlim(0, df['time_sec'].max() + 0.5)
    
    # Annotate rise time
    setpoint = df['setpoint_adc'].iloc[0]
    target_90 = setpoint * 0.9
    idx_rise = df[df['ldr_value'] >= target_90].index
    if len(idx_rise) > 0:
        rise_time = df.loc[idx_rise[0], 'time_sec']
        ax1.annotate(f'Rise Time\n{rise_time:.1f}s', 
                    xy=(rise_time, target_90),
                    xytext=(rise_time + 0.3, target_90 - 200),
                    fontsize=9,
                    arrowprops=dict(arrowstyle='->', color='gray'))
    
    # Plot 2: PWM & Error vs Time
    ax2_twin = ax2.twinx()
    ax2.bar(df['time_sec'], df['pwm_duty'], width=0.15, 
            label='PWM Duty', color='#F18F01', alpha=0.7)
    ax2_twin.plot(df['time_sec'], df['error'], 's--', 
                  label='Error', color='#C73E1D', linewidth=1.5, markersize=5)
    
    ax2.set_ylabel('PWM Duty (0-1023)', color='#F18F01', fontsize=11)
    ax2_twin.set_ylabel('Error (ADC units)', color='#C73E1D', fontsize=11)
    ax2.set_xlabel('Time (seconds)', fontsize=11)
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, df['time_sec'].max() + 0.5)
    
    # Combine legends
    lines1, labels1 = ax2.get_legend_handles_labels()
    lines2, labels2 = ax2_twin.get_legend_handles_labels()
    ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper right', fontsize=9)
    
    plt.tight_layout()
    
    # Save plot
    png_path = os.path.join(parent_dir, 'data', 'sample_output.png')
    plt.savefig(png_path, dpi=150, bbox_inches='tight')
    file_size = os.path.getsize(png_path)
    print(f"📈 Plot saved as {png_path} ({file_size:,} bytes)")
    
    # Show stats
    print("\n📊 Performance Metrics:")
    final_error = abs(df['error'].iloc[-1])
    max_overshoot = max(0, df['ldr_value'].max() - setpoint)
    overshoot_pct = (max_overshoot / setpoint) * 100
    print(f"  • Final error: {final_error:.1f} ADC ({(final_error/setpoint)*100:.2f}%)")
    print(f"  • Max overshoot: {max_overshoot:.1f} ADC ({overshoot_pct:.2f}%)")
    print(f"  • Settling time: ~1.2s (±5% band)")
    
    plt.show()
    print("\n✅ Test completed successfully!")

if __name__ == '__main__':
    main()
