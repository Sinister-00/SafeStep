#include <Wire.h>
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <MadgwickAHRS.h>

Madgwick filter;

const char *ssid = "Android_One";
const char *password = "hostelnet";
const int port = 8888;

const int MPU = 0x68; // MPU6050 I2C address
float AccX, AccY, AccZ;
float GyroX, GyroY, GyroZ;
float MagX, MagY, MagZ;
float roll, pitch, yaw;

WiFiServer server(port);
WiFiClient client;

void setup()
{
    Wire.begin(4, 5); // Use GPIO 4 (D2) for SDA and GPIO 5 (D1) for SCL
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

    // Connect to Wi-Fi network
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(1000);
        Serial.println("Connecting to WiFi...");
    }

    // Start the server
    server.begin();
}

void loop()
{
    // Check if a client has connected
    if (!client.connected())
    {
        client = server.available();
        if (client)
        {
            Serial.println("Client connected");
        }
    }

    // Read accelerometer data
    Wire.beginTransmission(MPU);
    Wire.write(0x3B);
    Wire.endTransmission(false);
    Wire.requestFrom(MPU, 6, true);
    AccX = (Wire.read() << 8 | Wire.read()) / 16384.0; // ±16 G range
    AccY = (Wire.read() << 8 | Wire.read()) / 16384.0;
    AccZ = (Wire.read() << 8 | Wire.read()) / 16384.0;

    AccX = AccX - 0.13;
    AccY = AccY - 3.99;
    AccZ = AccZ - 3.99;

    // Read gyroscope data
    Wire.beginTransmission(MPU);
    Wire.write(0x43);
    Wire.endTransmission(false);
    Wire.requestFrom(MPU, 6, true);
    GyroX = (Wire.read() << 8 | Wire.read()) / 200; // ±2,000°/s range
    GyroY = (Wire.read() << 8 | Wire.read()) / 200;
    GyroZ = (Wire.read() << 8 | Wire.read()) / 200;
//    GyroX= GyroX-406.0;
//    GyroY=GyroY-407.0;
//    GyroZ=GyroZ-406.0;
    
    // Read magnetometer data
    Wire.beginTransmission(MPU);
    Wire.write(0x03);
    Wire.endTransmission(false);
    Wire.requestFrom(MPU, 6, true);
    MagX = (Wire.read() << 8 | Wire.read()) / 16384.0; // ±16 G range
    MagY = (Wire.read() << 8 | Wire.read()) / 16384.0;
    MagZ = (Wire.read() << 8 | Wire.read()) / 16384.0;

    // Apply sensor fusion using Madgwick filter
    filter.updateIMU(GyroX, GyroY, GyroZ, AccX, AccY, AccZ);
    roll = filter.getRoll();
    pitch = filter.getPitch();
    yaw = filter.getYaw();

    // Send the orientation angles to the connected client
    client.print(AccX);
    client.print(",");
    client.print(AccY);
    client.print(",");
    client.print(AccZ);
    client.print(",");
    client.print(GyroX);
    client.print(",");
    client.print(GyroY);
    client.print(",");
    client.print(GyroZ);
    client.print(",");
    client.print(roll);
    client.print(",");
    client.print(pitch);
    client.print(",");
    client.print(yaw);
    client.println("");

    delay(10);
}