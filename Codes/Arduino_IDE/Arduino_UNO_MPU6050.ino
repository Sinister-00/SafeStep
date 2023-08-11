#include <Wire.h>
#include <MadgwickAHRS.h>

Madgwick filter;

const int MPU = 0x68; // MPU6050 I2C address
float AccX, AccY, AccZ;
float GyroX, GyroY, GyroZ;
float MagX, MagY, MagZ;
float roll, pitch, yaw;

void setup() {
  Serial.begin(19200);
  Wire.begin();
  Wire.beginTransmission(MPU);
  Wire.write(0x6B);
  Wire.write(0x00);
  
  Wire.endTransmission(true);
  
  // Configure Accelerometer Sensitivity - Full Scale Range (±16 G)
  Wire.beginTransmission(MPU);
  Wire.write(0x1C);
  Wire.write(0x18);
  Wire.endTransmission(true);
  
  // Configure Gyro Sensitivity - Full Scale Range (±2,000°/s)
  Wire.beginTransmission(MPU);
  Wire.write(0x1B);
  Wire.write(0x18);
  Wire.endTransmission(true);
  
  // Initialize Madgwick filter
  filter.begin(100); // Sample rate of 100 Hz
}

void loop() {
  // Read accelerometer data
  Wire.beginTransmission(MPU);
  Wire.write(0x3B);
  Wire.endTransmission(false);
  Wire.requestFrom(MPU, 6, true);
  AccX = (Wire.read() << 8 | Wire.read()) / 2048.0; // ±16 G range
  AccY = (Wire.read() << 8 | Wire.read()) / 2048.0;
  AccZ = (Wire.read() << 8 | Wire.read()) / 2048.0;
  

  AccX = AccX - 1.00;
  AccY = AccY + 0.03;
  AccZ = AccZ + 0.13;
  // Read gyroscope data
  Wire.beginTransmission(MPU);
  Wire.write(0x43);
  Wire.endTransmission(false);
  Wire.requestFrom(MPU, 6, true);
  GyroX = (Wire.read() << 8 | Wire.read()) / 16.4; // ±2,000°/s range
  GyroY = (Wire.read() << 8 | Wire.read()) / 16.4;
  GyroZ = (Wire.read() << 8 | Wire.read()) / 16.4;
  
  // Read magnetometer data
  Wire.beginTransmission(MPU);
  Wire.write(0x03);
  Wire.endTransmission(false);
  Wire.requestFrom(MPU, 6, true);
  MagX = (Wire.read() << 8 | Wire.read()) / 2048.0; // ±16 G range
  MagY = (Wire.read() << 8 | Wire.read()) / 2048.0;
  MagZ = (Wire.read() << 8 | Wire.read()) / 2048.0;
  
  // Apply sensor fusion using Madgwick filter
  filter.updateIMU(GyroX, GyroY, GyroZ, AccX, AccY, AccZ);
  // roll = filter.getRoll();
  // pitch = filter.getPitch();
  // yaw = filter.getYaw();
  roll = atan2(AccY, AccZ) * (180.0 / PI);
  pitch = atan(-AccX / sqrt(AccY * AccY + AccZ * AccZ)) * (180.0 / PI);
  yaw = atan2(MagY * cos(roll) - MagZ * sin(roll), MagX * cos(pitch) + MagY * sin(pitch) * sin(roll) + MagZ * sin(pitch) * cos(roll)) * (180.0 / PI);
  
  // Print the orientation angles
  Serial.print(AccX);
  Serial.print(",");
  Serial.print(AccY);
  Serial.print(",");
  Serial.print(AccZ);
  Serial.print(",");
  Serial.print(GyroX);
  Serial.print(",");
  Serial.print(GyroY);
  Serial.print(",");
  Serial.print(GyroZ);
  Serial.print(",");
  Serial.print(roll);
  Serial.print(",");
  Serial.print(pitch);
  Serial.print(",");
  Serial.print(yaw);
  Serial.println("");

  
  delay(10);
}
