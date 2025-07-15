// Include the Wire library for I2C communication with the servo controller.
#include <Wire.h>

// --- Configuration ---
// I2C Slave address for the Robokits controller board.
#define SERVO_CONTROLLER_1 (16 >> 1)

// The total number of servos connected to the controller.
const int TOTAL_SERVOS = 18;

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
    // If we have an I2C error, we shouldn't continue trying.
    // The error will be printed inside setServo.
  }

  Serial.println("\nInitialization complete. Ready for commands.");
}

/**
 * @brief Main loop. Listens for and processes commands sent from Python.
 */
void loop() {
  if (Serial.available() > 0) {
    char incomingChar = Serial.read();

    if (incomingChar == '\n') {
      Serial.print("Command received: ");
      Serial.println(serialCommand);

      int commaIndex = serialCommand.indexOf(',');

      if (commaIndex != -1) {
        String indexStr = serialCommand.substring(0, commaIndex);
        String angleStr = serialCommand.substring(commaIndex + 1);

        int servoIndex = indexStr.toInt();
        int angle = angleStr.toInt();

        // We pass 'false' because this is a regular command, not a setup check.
        setServo(servoIndex, angle, false);

        Serial.print("Moved servo ");
        Serial.print(servoIndex);
        Serial.print(" to ");
        Serial.print(angle);
        Serial.println(" degrees.");
      } else {
        Serial.println("Error: Invalid command format. Expected 'index,angle'.");
      }

      serialCommand = "";
    } else {
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

  // *** THIS IS THE IMPORTANT NEW PART ***
  // Check the status of the I2C transmission.
  byte error = Wire.endTransmission();

  if (error != 0) {
    Serial.print("I2C Error on Servo ");
    Serial.print(index);
    Serial.print(". Error code: ");
    Serial.println(error);
    Serial.println("--> CHECK WIRING AND POWER for the servo controller!");

    // During setup, we only want to show the error once.
    if (isSetupCheck) {
      // This will hang the loop so you just see the error message.
      while(1); 
    }
  }
}
