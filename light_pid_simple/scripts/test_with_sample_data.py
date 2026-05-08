#!/usr/bin/env python3
"""
Test script to generate sample output using sample_data.csv
Used for CI/CD verification and demonstration
"""
import pandas as pd
import matplotlib.pyplot as plt
import os

def main():
    # Ensure we're in the right directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    data_dir = os.path.join(project_dir, 'data')
    
    # Load sample data
    csv_path = os.path.join(data_dir, 'sample_data.csv')
    output_png = os.path.join(data_dir, 'sample_output.png')
    
    print(f"📂 Loading sample data from {csv_path}")
    df = pd.read_csv(csv_path)
    
    # Add time column
    df['time_sec'] = df['time_ms'] / 1000.0
    
    print(f"📊 Data points: {len(df)}")
    print(f"⏱️  Duration: {df['time_sec'].max():.1f} seconds")
    print(f"🎯 Setpoint: {df['setpoint_lux'].iloc[0]:.1f} lux")
    print(f"📈 Final lux: {df['actual_lux'].iloc[-1]:.1f}")
    print(f"🔧 Final PWM: {df['pwm_duty'].iloc[-1]}")
    
    # Create plots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    
    # Plot 1: Lux vs Time
    ax1.plot(df['time_sec'], df['actual_lux'], label='Actual Lux', color='#2E86AB', linewidth=2, marker='o', markersize=4)
    ax1.axhline(y=df['setpoint_lux'].iloc[0], color='#A23B72', linestyle='--', label='Setpoint (300 lux)', linewidth=2)
    ax1.set_ylabel('Illuminance (lux)', fontsize=11)
    ax1.legend(loc='upper right', fontsize=10)
    ax1.grid(True, alpha=0.3, linestyle=':')
    ax1.set_title('🔆 Light Intensity PID Control Response\n(Sample Data - Discrete PID System)', fontsize=12, fontweight='bold')
    ax1.set_ylim(0, max(df['actual_lux']) * 1.2)
    
    # Annotate key points
    rise_time_idx = (df['actual_lux'] >= df['setpoint_lux'].iloc[0] * 0.9).idxmax()
    settling_time_idx = (abs(df['actual_lux'] - df['setpoint_lux'].iloc[0]) <= 5).idxmax()
    
    ax1.annotate(f'Rise Time (~90%)\n{df["time_sec"].iloc[rise_time_idx]:.1f}s',
                xy=(df['time_sec'].iloc[rise_time_idx], df['actual_lux'].iloc[rise_time_idx]),
                xytext=(df['time_sec'].iloc[rise_time_idx] + 0.5, df['actual_lux'].iloc[rise_time_idx] + 30),
                arrowprops=dict(arrowstyle='->', color='gray'),
                fontsize=9, ha='left')
    
    # Plot 2: PWM & Error vs Time
    ax2_twin = ax2.twinx()
    
    pwm_line = ax2.plot(df['time_sec'], df['pwm_duty'], label='PWM Duty', color='#F18F01', linewidth=2, marker='s', markersize=4)
    error_line = ax2_twin.plot(df['time_sec'], df['error'], label='Error', color='#C73E1D', linestyle=':', linewidth=2)
    
    ax2.set_ylabel('PWM Duty (0-1023)', color='#F18F01', fontsize=11)
    ax2_twin.set_ylabel('Error (lux)', color='#C73E1D', fontsize=11)
    ax2.set_xlabel('Time (seconds)', fontsize=11)
    ax2.grid(True, alpha=0.3, linestyle=':')
    
    # Combine legends
    lines1, labels1 = ax2.get_legend_handles_labels()
    lines2, labels2 = ax2_twin.get_legend_handles_labels()
    ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper right', fontsize=10)
    
    # Colorize twin y-axis labels
    ax2.tick_params(axis='y', labelcolor='#F18F01')
    ax2_twin.tick_params(axis='y', labelcolor='#C73E1D')
    
    plt.tight_layout()
    
    # Save figure
    plt.savefig(output_png, dpi=150, bbox_inches='tight', facecolor='white')
    print(f"✅ Plot saved to {output_png}")
    
    # Print analysis
    print("\n📊 PID Performance Analysis:")
    print(f"   • Initial Error: {df['error'].iloc[0]:+.1f} lux")
    print(f"   • Final Error: {df['error'].iloc[-1]:+.1f} lux")
    print(f"   • Max Overshoot: {df['actual_lux'].max() - df['setpoint_lux'].iloc[0]:+.1f} lux")
    print(f"   • Settling Time: ~{df['time_sec'].iloc[settling_time_idx]:.1f}s (±5 lux)")
    print(f"   • Steady State PWM: {df['pwm_duty'].iloc[-1]}")
    
    # Verify file was created
    if os.path.exists(output_png):
        file_size = os.path.getsize(output_png)
        print(f"\n✓ Verification: PNG file exists ({file_size:,} bytes)")
        return 0
    else:
        print("\n✗ Error: PNG file was not created!")
        return 1

if __name__ == '__main__':
    exit(main())
