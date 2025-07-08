import serial
import time

# --- Configuration ---
# Update this to your Arduino's actual COM port
SERIAL_PORT = 'COM6' 
BAUD_RATE = 960090
# This must match the TOTAL_SERVOS constant in your Arduino sketch
# Changed from 18 to 6 as requested.
TOTAL_SERVOS = 6

def connect_to_arduino(port, baud_rate):
    """
    Establishes a serial connection and listens for initial messages.
    """
    try:
        print(f"Connecting to Arduino on {port} at {baud_rate} bps...")
        # Add a write_timeout to prevent the script from freezing indefinitely.
        ser = serial.Serial(port, baud_rate, timeout=2, write_timeout=2)
        
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

def send_positions_command(serial_connection, positions_string):
    """
    Formats and sends a command string of all servo positions to the Arduino.
    
    Args:
        serial_connection: The active PySerial object.
        positions_string (str): A comma-separated string of angles.
    """
    if serial_connection and serial_connection.is_open:
        # The command is already formatted, just add the newline terminator.
        command = f"{positions_string}\n"
        
        try:
            # Encode the string to bytes and send it.
            serial_connection.write(command.encode('utf-8'))
            print(f"Sent positions: {positions_string}")
            
            # Wait for a confirmation response from the Arduino.
            response = serial_connection.readline().decode('utf-8').strip()
            if response:
                print(f"Arduino says: {response}")
            else:
                print("No response from Arduino.")

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

    print("\n--- Python Multi-Servo Controller ---")
    print(f"Enter {TOTAL_SERVOS} comma-separated angle values (e.g., '90,45,180,...').")
    print("The first value is for servo 0, the second for servo 1, and so on.")
    print("Type 'exit' to quit.")
    
    try:
        while True:
            user_input = input("\nEnter all servo positions: ")
            
            if user_input.lower() == 'exit':
                print("Closing serial port and exiting.")
                break

            try:
                # Remove any accidental whitespace from the input string.
                user_input = user_input.replace(" ", "")
                parts = user_input.split(',')
                
                # Validate that the correct number of positions were entered.
                if len(parts) != TOTAL_SERVOS:
                    raise ValueError(f"Invalid input. Please provide exactly {TOTAL_SERVOS} values. You provided {len(parts)}.")
                
                # Validate that each value is a number between 0 and 180.
                for part in parts:
                    angle = int(part)
                    if not (0 <= angle <= 180):
                        raise ValueError(f"Invalid angle '{angle}'. All angles must be between 0 and 180.")

                # If all validation passes, send the command string to the Arduino.
                send_positions_command(arduino_ser, user_input)

            except ValueError as e:
                # Catch errors from parsing (e.g., text instead of numbers) or validation.
                print(f"Input Error: {e}")
            
    finally:
        if arduino_ser and arduino_ser.is_open:
            arduino_ser.close()
            print("Serial port closed.")

if __name__ == "__main__":
    main()

