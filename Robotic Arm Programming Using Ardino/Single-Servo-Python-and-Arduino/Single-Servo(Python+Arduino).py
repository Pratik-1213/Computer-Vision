import serial
import time

# --- Configuration ---
SERIAL_PORT = 'COM6' 
BAUD_RATE = 9600

def connect_to_arduino(port, baud_rate):
    """
    Establishes a serial connection and listens for initial messages.
    """
    try:
        print(f"Connecting to Arduino on {port} at {baud_rate} bps...")
        # Add a write_timeout to prevent the script from freezing indefinitely.
        ser = serial.Serial(port, baud_rate, timeout=1, write_timeout=1)
        
        # Give the Arduino time to reset and start sending messages.
        print("Connection established. Waiting for Arduino to boot...")
        time.sleep(2) 
        
        # Read any startup messages from the Arduino (like setup errors).
        print("--- Arduino Startup Log ---")
        while ser.in_waiting > 0:
            try:
                line = ser.readline().decode('utf-8').strip()
                if line:
                    print(line)
            except Exception as e:
                print(f"Error reading line: {e}")
        print("---------------------------")
        
        print("\nConnection successful!")
        return ser
        
    except serial.SerialException as e:
        print(f"Error: Could not open serial port {port}.")
        print(f"Details: {e}")
        print("Please ensure the Arduino is connected, the correct port is selected,")
        print("and no other program (like the Arduino IDE's Serial Monitor) is using it.")
        return None

def send_command(serial_connection, servo_index, angle):
    """
    Formats and sends a command to the Arduino to move a servo.
    """
    if serial_connection and serial_connection.is_open:
        command = f"{servo_index},{angle}\n"
        try:
            # Encode the string to bytes and send it.
            serial_connection.write(command.encode('utf-8'))
            print(f"Sent: Move Servo {servo_index} to {angle}°")
            
            # Wait for a confirmation response from the Arduino.
            response = serial_connection.readline().decode('utf-8').strip()
            if response:
                print(f"Arduino says: {response}")
            else:
                print("No response from Arduino. The servo may or may not have moved.")

        except serial.SerialTimeoutException:
             print("Error: Write to serial port timed out. The Arduino may be frozen.")
        except serial.SerialException as e:
            print(f"Error writing to serial port: {e}")
    else:
        print("Cannot send command: Serial connection is not open.")

def main():
    """
    Main function to run the command-line interface for controlling the arm.
    """
    arduino_ser = connect_to_arduino(SERIAL_PORT, BAUD_RATE)
    
    if not arduino_ser:
        return # Exit if connection failed

    print("\n--- Python Servo Controller ---")
    print("Enter commands in the format 'servo,angle' (e.g., '5,90').")
    print("Type 'exit' to quit.")
    
    try:
        while True:
            user_input = input("\nEnter command: ")
            
            if user_input.lower() == 'exit':
                print("Closing serial port and exiting.")
                break

            try:
                parts = user_input.split(',')
                if len(parts) != 2:
                    raise ValueError("Invalid format. Please use 'servo,angle'.")
                
                servo_id = int(parts[0].strip())
                angle_val = int(parts[1].strip())

                if not (0 <= servo_id < 18):
                     raise ValueError("Servo index must be between 0 and 17.")
                if not (0 <= angle_val <= 180):
                     raise ValueError("Angle must be between 0 and 180.")

                send_command(arduino_ser, servo_id, angle_val)

            except ValueError as e:
                print(f"Error: {e}")
            
    finally:
        if arduino_ser and arduino_ser.is_open:
            arduino_ser.close()

if __name__ == "__main__":
    main()
