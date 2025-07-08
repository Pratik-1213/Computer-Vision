// Include the Wire library for I2C communication, which is used to talk to the servo controller.
#include <Wire.h>

// --- Configuration ---
// I2C Slave address for the Robokits controller board.
// This is for servos 1-18. The address is 0x08.
#define SERVO_CONTROLLER_1 (16 >> 1)

// The total number of servos connected to the controller.
const int TOTAL_SERVOS = 18;

/**
 * @brief Initializes the Arduino, sets up Serial/I2C, and positions servos.
 * - Servos 0 and 1 are set to 90 degrees.
 * - Servos 2 through 17 are set to 90 degrees.
 */
void setup() {
  // Start serial communication for debugging and receiving commands from the Serial Monitor.
  // Make sure to set the Serial Monitor's baud rate to 9600.
  Serial.begin(9600);

  // Initialize the I2C bus to communicate with the servo controller.
  Wire.begin();

  // These values configure the I2C clock speed.
  // It's best to keep them from your original code as they are specific to your hardware.
  TWSR = 3;
  TWBR = 18;

  // Wait a moment for everything to initialize.
  delay(500);

  // --- Initialize servos ---
  Serial.println("Initializing all servos to 90 degrees...");
  for (int i = 0; i < TOTAL_SERVOS; i++) {
    setServo(i, 90);
    delay(20); // Small delay between commands to the controller.
  }
  Serial.println("Initialization complete.");

  // Print a welcome message to the Serial Monitor to let the user know it's ready.
  Serial.println();
  Serial.println("--- Servo Control Ready ---");
  Serial.println("Enter the Servo Index (0 - 5)");
  Serial.println("Enter command as '<servo><angle>' (e.g., '0 90' or '1 180') and press Enter.");
  Serial.println(); // Add a blank line for readability.
}

/**
 * @brief Main loop, constantly checks for new input from the Serial Monitor.
 * Listens for commands in the format "<servo_index><angle>".
 */
void loop() {
  // Check if there is any data available to read from the Serial Monitor.
  if (Serial.available() > 0) {
    // Read the servo index (the first integer in the input).
    int servoIndex = Serial.parseInt();

    // Check if there is a second number (the angle) waiting.
    // We can do this by peeking for a space or a digit.
    if (Serial.peek() == ' ') {
      // Read the angle (the second integer).
      int angle = Serial.parseInt();

      // Clear any remaining characters (like newline) from the input buffer.
      while (Serial.available() > 0) {
        Serial.read();
      }

      // --- Validate the input ---
      // We only want to control servos 0 and 1.
      if (servoIndex == 0 || servoIndex == 1 || servoIndex == 2 || servoIndex == 3 || servoIndex == 4 || servoIndex == 5) {
        // Echo the command back to the user.
        Serial.print("Received command. Moving Servo ");
        Serial.print(servoIndex);
        Serial.print(" to angle: ");
        Serial.println(angle);

        // Call the function to move the specified servo to the specified angle.
        setServo(servoIndex, angle);
      } else {
        // If the user enters an invalid servo index, print an error message.
        Serial.print("Invalid servo index: ");
        Serial.print(servoIndex);
        Serial.println(". Please use 0 or 1.");
      }
    }

    // Add a small delay to prevent spamming commands.
    delay(50);
  }
}

/**
 * @brief Sends a command to the Robokits I2C servo controller to set a servo's angle.
 *
 * @param index The servo number (0-17).
 * @param angleDeg The target angle in degrees (0-180).
 */
void setServo(int index, int angleDeg) {
  // Constrain the angle to be within the valid range of 0 to 180 degrees.
  angleDeg = constrain(angleDeg, 0, 180);

  // This logic from your original code reverses the direction of specific servos.
  // Kept for consistency. Servo 1 will be reversed.
  if (index == 1 || index == 3 || index == 4 || index == 5) {
    angleDeg = 180 - angleDeg;
  }

  // Map the 0-180 degree angle to the servo's pulse width range in microseconds (500-2500 us).
  int pulse_us = map(angleDeg, 0, 180, 500, 2500);

  // The servo controller expects a PWM value, which is calculated from the pulse width.
  int pwm_val = ((pulse_us - 2) * 2) - 1000;

  // The servo number sent over I2C is 1-based.
  uint8_t servo_num = index + 1;

  // Begin an I2C transmission to the servo controller's address.
  Wire.beginTransmission(SERVO_CONTROLLER_1);

  // Send the data:
  Wire.write(servo_num - 1);  // 1. The servo channel on the controller.
  Wire.write(pwm_val >> 8);   // 2. The high byte of the PWM value.
  Wire.write(pwm_val & 0xFF); // 3. The low byte of the PWM value.

  // End the transmission, sending the data to the controller.
  Wire.endTransmission();
}
