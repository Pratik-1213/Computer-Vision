#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

#define SERVOMIN  150
#define SERVOMAX  600
#define ANGLE_STEP 1

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x40);

const int servoToChannel[6] = {0, 1, 2, 3, 4, 5};
float servoAngles[6] = {90, 90, 90, 90, 90, 90};

String inputString = "";
bool stringComplete = false;
int speedDelay = 10;

void setup() {
  Serial.begin(115200);
  Wire.begin(21, 22);
  pwm.begin();
  pwm.setPWMFreq(50);

  delay(500);
  for (int i = 0; i < 6; i++) {
    setServo(i, servoAngles[i]);
    delay(200);
  }

  Serial.println("Enter 6 comma-separated angles like: 90,90,90,90,90,90");
  Serial.println("Or type 'ST' to set all servos to 60 degrees.");
}

void loop() {
  serialInputHandler();

  if (stringComplete) {
    processSerialInput(inputString);
    inputString = "";
    stringComplete = false;
  }
}

void setServo(int index, float angle) {
  if (index < 0 || index >= 6) return;

  angle = constrain(angle, 0, 180);
  uint16_t pulseLen = map(angle, 0, 180, SERVOMIN, SERVOMAX);
  int channel = servoToChannel[index];

  pwm.setPWM(channel, 0, pulseLen);
}

void smoothMove(int index, float currentAngle, float targetAngle) {
  if (currentAngle == targetAngle) return;

  float stepSize = 0.5;
  float step = (targetAngle > currentAngle) ? stepSize : -stepSize;

  for (float angle = currentAngle; abs(angle - targetAngle) >= stepSize; angle += step) {
    setServo(index, angle);
    delay(speedDelay);
  }
  setServo(index, targetAngle);
}

void serialInputHandler() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    if (inChar == '\n') {
      stringComplete = true;
    } else {
      inputString += inChar;
    }
  }
}

void processSerialInput(String data) {
  data.trim();
  data.toUpperCase();  // Convert input to uppercase

  if (data == "ST") {
    Serial.println("Setting all servos to 60 degrees.");
    for (int i = 0; i < 6; i++) {
      smoothMove(i, servoAngles[i], 60);
      servoAngles[i] = 60;
      Serial.printf("Servo %d: 60\n", i + 1);
    }
    return;
  }

  int angles[6] = {0};
  int index = 0;
  char *token;
  char inputBuffer[64];
  data.toCharArray(inputBuffer, sizeof(inputBuffer));

  token = strtok(inputBuffer, ",");
  while (token != NULL && index < 6) {
    angles[index++] = atoi(token);
    token = strtok(NULL, ",");
  }

  if (index == 6) {
    Serial.println("Moving Servos to:");
    for (int i = 0; i < 6; i++) {
      Serial.printf("Servo %d: %d\n", i + 1, angles[i]);
      smoothMove(i, servoAngles[i], angles[i]);
      servoAngles[i] = angles[i];
    }
  } else {
    Serial.println("Invalid input. Enter exactly 6 comma-separated angles like: 90,90,90,90,90,90");
  }
}
