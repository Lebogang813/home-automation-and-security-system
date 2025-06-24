#include <ArduinoJson.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <OneWire.h>
#include <DallasTemperature.h>

// Sensor Definitions
#define ONE_WIRE_BUS 4  
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

// WiFi Credentials
const char* ssid = "Bernet S21 FE";
const char* password = "123345678";
const char* serverUrl = "http://192.168.0.153:5000/update"; // Replace with actual server IP

WiFiClient client;
HTTPClient http;

// Define digital output (DO) pins
#define Infra_red 14
#define LDR_1 36  // analog pin
#define LDR_2 39
#define humidity 34 // analog pin

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected! IP Address: ");
  Serial.println(WiFi.localIP());

  sensors.begin();

  pinMode(Infra_red , INPUT);
  pinMode(LDR_1, INPUT);  // LDR sensor pin
  pinMode(LDR_2, INPUT);
  pinMode(humidity, INPUT); // Soil moisture sensor pin
}

void loop() {
  sensors.requestTemperatures();
  float Temperature = sensors.getTempCByIndex(0);  // Get DS18B20 temperature

  bool irDetected = digitalRead(Infra_red);  
  int ldrValue1 = analogRead(LDR_1);  // LDR sensor light intensity value (analog)
  int ldrValue2 = analogRead(LDR_2);
  int humidityy = analogRead(humidity); // moisture sensor status


  // Debugging Prints
  Serial.println("DS18B20 Temperature: " + String(Temperature));
  
  Serial.println("LDR_1: " + String(ldrValue1));  // Print LDR value
  Serial.println("humidity level: " + String(humidityy));
  Serial.println("LDR_2: " + String(ldrValue2));
  Serial.println("Infrared Sensor: " + String(irDetected));

  StaticJsonDocument<200> jsonData;
  jsonData["DS18B20_Temperature"] = Temperature;
  
  jsonData["LDR_1"] = ldrValue1;  // Include LDR intensity in JSON data
  jsonData["Humidity"] = humidityy;
  jsonData["LDR_2"] = ldrValue2; 
  jsonData["InfraRed"] = irDetected;

  String jsonOutput;
  serializeJson(jsonData, jsonOutput);
  
  http.begin(client, serverUrl);
  http.addHeader("Content-Type", "application/json");

  Serial.println("Sending JSON Data...");
  Serial.println(jsonOutput);

  int httpResponseCode = http.POST(jsonOutput);
  Serial.println("Server Response Code: " + String(httpResponseCode));

  if (httpResponseCode > 0) {
    Serial.println("Server Response: " + http.getString());
  } else {
    Serial.println("Error Sending Request!");
  }

  http.end();
  delay(5000);
}
