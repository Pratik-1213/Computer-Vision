// Include the Wire library for I2C communication, which is used to talk to the servo controller.
#include <Wire.h>

// --- Configuration ---
// I2C Slave address for the Robokits controller board.
// This is for servos 1-18. The address is 0x08.
#define SERVO_CONTROLLER_1 (16 >> 1)

// The index of the primary servo you want to control via Serial Monitor.
const int SERVO_INDEX = 0;

// The total number of servos connected to the controller.
const int TOTAL_SERVOS = 18;

/**
 * @brief Initializes the Arduino, sets other servos to 90 degrees, and starts Serial/I2C.
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

  // --- Initialize other servos to 90 degrees ---
  Serial.println("Initializing other servos to 90 degrees...");
  for (int i = 0; i < TOTAL_SERVOS; i++) {
    // We only want to initialize the servos that are NOT the main one we're controlling.
    if (i != SERVO_INDEX) {
      setServo(i, 90);
      delay(20); // Small delay between commands to the controller.
    }
  }
  Serial.println("Initialization complete.");

  // Also set the primary servo to 90 degrees to start.
  setServo(SERVO_INDEX, 90);

  // Print a welcome message to the Serial Monitor to let the user know it's ready.
  Serial.println();
  Serial.println("--- Servo Control Ready ---");
  Serial.println("Controlling Servo 0. Enter an angle (0-180) and press Enter.");
  Serial.println(); // Add a blank line for readability.
}

/**
 * @brief Main loop, constantly checks for new input from the Serial Monitor for the primary servo.
 */
void loop() {
  // Check if there is any data available to read from the Serial Monitor.
  if (Serial.available() > 0) {
    // Read the incoming text as an integer. This will read numbers like "90", "120", etc.
    int angle = Serial.parseInt();

    // The Serial.parseInt() function might leave a newline character in the buffer.
    // This loop clears any remaining characters to prevent misreading the next command.
    while (Serial.available() > 0) {
      Serial.read();
    }

    // Echo the command back to the user so they can see what was received.
    Serial.print("Received command. Moving Servo ");
    Serial.print(SERVO_INDEX);
    Serial.print(" to angle: ");
    Serial.println(angle);

    // Call the function to move the servo to the specified angle.
    setServo(SERVO_INDEX, angle);

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
  // It's kept here for consistency. It won't affect the 90-degree setting (180-90=90).
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
  Wire.endTransmission();}
