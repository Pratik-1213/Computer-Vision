#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>
#include "BluetoothSerial.h"

BluetoothSerial SerialBT;

#define MAX_STEPS 50
#define SERVOMIN  150
#define SERVOMAX  600
#define ANGLE_STEP 1   // Smaller step for smoothness

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x40);

// Correct channel mapping for all 6 servos
const int servoToChannel[6] = {0, 1, 2, 3, 4, 5};

float servoAngles[6] = {90, 90, 90, 90, 90, 90};
float recordedAngles[MAX_STEPS][6];
int stepsCount = 0;

unsigned long lastMoveTime = 0;
int speedDelay = 10;   // Speed delay (adjust for faster/slower smoothness)
int currentCommand = 0;

bool isPlaying = false;
bool isPaused = false;
int playStepIndex = 0;

void setup() {
  Serial.begin(115200);
  SerialBT.begin("ESP32_Arm");

  Wire.begin(21, 22);    // SDA = 21, SCL = 22
  pwm.begin();
  pwm.setPWMFreq(50);

  delay(500);

  for (int i = 0; i < 6; i++) {
    setServo(i, servoAngles[i]);
    delay(200);
  }
}

void loop() {
  if (SerialBT.available()) {
    currentCommand = SerialBT.read();

    if (currentCommand > 100 && currentCommand < 250) {
      speedDelay = currentCommand / 10;
      currentCommand = 0;
    }
    else if (currentCommand == 12) { // Save Step
      if (stepsCount < MAX_STEPS) {
        for (int i = 0; i < 6; i++) {
          recordedAngles[stepsCount][i] = servoAngles[i];
        }
        stepsCount++;
      }
      currentCommand = 0;
    }
    else if (currentCommand == 14) { // Play Steps
      isPlaying = true;
      isPaused = false;
      playStepIndex = 0;
      currentCommand = 0;
    }
    else if (currentCommand == 15) { // Pause
      isPaused = true;
      currentCommand = 0;
    }
    else if (currentCommand == 13) { // Reset
      float servorest[6] = {90, 90, 90, 90, 90, 90};
      for (int i = 0; i < 6; i++) {
        smoothMove(i, servoAngles[i], servorest[i]);
        servoAngles[i] = servorest[i];
      }
      stepsCount = 0;
      isPlaying = false;
      isPaused = false;
      playStepIndex = 0;
      currentCommand = 0;
    }
    else if (currentCommand >= 16 && currentCommand <= 27) {
      int servoIndex = (currentCommand - 16) / 2;
      int direction = (currentCommand % 2 == 0) ? 1 : -1;

      // Move continuously while button is held
      while (SerialBT.available() == 0) {
        servoAngles[servoIndex] += direction * ANGLE_STEP;
        servoAngles[servoIndex] = constrain(servoAngles[servoIndex], 0, 180);
        setServo(servoIndex, servoAngles[servoIndex]);
        delay(speedDelay);
      }

      currentCommand = 0;
    }
  }

  if (isPlaying && !isPaused) {
    if (playStepIndex < stepsCount) {
      for (int i = 0; i < 6; i++) {
        smoothMove(i, servoAngles[i], recordedAngles[playStepIndex][i]);
        servoAngles[i] = recordedAngles[playStepIndex][i];
      }
      playStepIndex++;
      delay(300);
    } else {
      isPlaying = false;
    }
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
