#!/usr/bin/env python3
"""
CSV Format Validator for Light PID Control System
Validates that CSV files have the correct format and data types
"""
import csv
import sys
import os

def validate_csv(csv_path):
    """Validate CSV file format and content"""
    print(f"🔍 Validating: {csv_path}")
    
    if not os.path.exists(csv_path):
        print(f"  ✗ File does not exist!")
        return False
    
    try:
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            
            # Check headers
            expected_headers = ['time_ms', 'setpoint_lux', 'actual_lux', 'pwm_duty', 'error']
            if reader.fieldnames != expected_headers:
                print(f"  ✗ Invalid headers!")
                print(f"    Expected: {expected_headers}")
                print(f"    Got: {reader.fieldnames}")
                return False
            
            print(f"  ✓ Headers valid: {', '.join(expected_headers)}")
            
            # Validate data rows
            row_count = 0
            errors = []
            
            for i, row in enumerate(reader, start=2):  # Start at 2 (header is row 1)
                row_count += 1
                
                # Type validation
                try:
                    time_ms = int(row['time_ms'])
                    setpoint = float(row['setpoint_lux'])
                    lux = float(row['actual_lux'])
                    pwm = int(row['pwm_duty'])
                    error = float(row['error'])
                    
                    # Range validation
                    if time_ms < 0:
                        errors.append(f"Row {i}: time_ms cannot be negative")
                    if lux < 0:
                        errors.append(f"Row {i}: lux cannot be negative")
                    if pwm < 0 or pwm > 1023:
                        errors.append(f"Row {i}: PWM {pwm} out of range (0-1023)")
                    
                    # Consistency check
                    expected_error = setpoint - lux
                    if abs(error - expected_error) > 0.2:
                        errors.append(f"Row {i}: Error mismatch (got {error}, expected {expected_error:.1f})")
                
                except ValueError as e:
                    errors.append(f"Row {i}: Type conversion error - {e}")
            
            if errors:
                print(f"  ✗ Found {len(errors)} validation errors:")
                for err in errors[:5]:  # Show first 5 errors
                    print(f"    • {err}")
                if len(errors) > 5:
                    print(f"    ... and {len(errors) - 5} more")
                return False
            
            print(f"  ✓ Data validation passed ({row_count} rows)")
            
            # Additional stats
            if row_count > 0:
                print(f"  ℹ️  Sample: First row time_ms={int(row['time_ms'])}, Last row time_ms={time_ms}")
            
            return True
    
    except Exception as e:
        print(f"  ✗ Error reading file: {e}")
        return False

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    data_dir = os.path.join(project_dir, 'data')
    
    # Find all CSV files
    csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
    
    if not csv_files:
        print("⚠️  No CSV files found in data/ directory")
        return 1
    
    print(f"📁 Found {len(csv_files)} CSV file(s)\n")
    
    all_valid = True
    for csv_file in csv_files:
        csv_path = os.path.join(data_dir, csv_file)
        if not validate_csv(csv_path):
            all_valid = False
        print()
    
    if all_valid:
        print("✅ All CSV files are valid!")
        return 0
    else:
        print("❌ Some CSV files have validation errors")
        return 1

if __name__ == '__main__':
    sys.exit(main())
