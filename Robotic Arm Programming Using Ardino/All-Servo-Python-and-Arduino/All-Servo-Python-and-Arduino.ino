// Include the Wire library for I2C communication with the servo controller.
#include <Wire.h>

// --- Configuration ---
// I2C Slave address for the Robokits controller board.
#define SERVO_CONTROLLER_1 (16 >> 1)

// The total number of servos connected to the controller.
const int TOTAL_SERVOS = 6;

// A string to store the incoming command from Python.
String serialCommand; 

/**
 * @brief Initializes the Arduino, sets servos to 90 degrees, and starts Serial/I2C.
 */
void setup() {
  // Start serial communication for receiving commands from Python.
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }

  // Initialize the I2C bus to communicate with the servo controller.
  Wire.begin();

  // These values configure the I2C clock speed.
  TWSR = 3;
  TWBR = 18;

  delay(500);

  Serial.println("Arduino boot complete. Initializing servos...");

  // --- Initialize all servos to a default 90-degree position ---
  for (int i = 0; i < TOTAL_SERVOS; i++) {
    // We pass 'true' to indicate this is a setup check.
    setServo(i, 90, true); 
    delay(20); 
    // If we have an I2C error, the program will halt and display an error.
  }

  Serial.println("\nInitialization complete. Ready for commands.");
}

/**
 * @brief Main loop. Listens for and processes a comma-separated string of servo positions.
 */
void loop() {
  if (Serial.available() > 0) {
    char incomingChar = Serial.read();

    // Check if the character is a newline, which signifies the end of a command.
    if (incomingChar == '\n') {
      Serial.print("Command string received: ");
      Serial.println(serialCommand);

      int servoIndex = 0;
      int lastIndex = 0;

      // Loop through the command string to find commas and parse values.
      for (int i = 0; i < serialCommand.length(); i++) {
        if (serialCommand.charAt(i) == ',') {
          // Extract the value between the last comma (or start) and this one.
          String angleStr = serialCommand.substring(lastIndex, i);
          int angle = angleStr.toInt();

          // Move the servo if the index is within our total servo count.
          if (servoIndex < TOTAL_SERVOS) {
            setServo(servoIndex, angle, false);
          }

          servoIndex++;
          lastIndex = i + 1; // Update the starting point for the next value.
        }
      }

      // Handle the very last value in the string (after the last comma).
      String angleStr = serialCommand.substring(lastIndex);
      int angle = angleStr.toInt();
      if (servoIndex < TOTAL_SERVOS) {
        setServo(servoIndex, angle, false);
      }

      // Send one confirmation message after all servos are moved.
      Serial.println("All servo positions updated based on command.");

      // Clear the command string to be ready for the next one.
      serialCommand = "";
    } else {
      // If it's not a newline, append the character to our command string.
      // We also ignore carriage returns for better cross-platform compatibility.
      if (incomingChar != '\r') {
        serialCommand += incomingChar;
      }
    }
  }
}

/**
 * @brief Sends a command to the I2C servo controller and CHECKS for errors.
 * * @param index The servo number (0-17).
 * @param angleDeg The target angle in degrees (0-180).
 * @param isSetupCheck A flag to print a more specific error during setup.
 */
void setServo(int index, int angleDeg, bool isSetupCheck) {
  angleDeg = constrain(angleDeg, 0, 180);

  if (index == 1 || index == 3 || index == 4 || index == 5) {
    angleDeg = 180 - angleDeg;
  }

  int pulse_us = map(angleDeg, 0, 180, 500, 2500);
  int pwm_val = ((pulse_us - 2) * 2) - 1000;
  uint8_t servo_num = index + 1;

  Wire.beginTransmission(SERVO_CONTROLLER_1);
  Wire.write(servo_num - 1);
  Wire.write(pwm_val >> 8);
  Wire.write(pwm_val & 0xFF);

  byte error = Wire.endTransmission();

  if (error != 0) {
    Serial.print("I2C Error on Servo ");
    Serial.print(index);
    Serial.print(". Error code: ");
    Serial.println(error);
    Serial.println("--> CHECK WIRING AND POWER for the servo controller!");

    if (isSetupCheck) {
      // This will hang the program so you only see the error message on startup.
      while(1); 
    }
  }
}
