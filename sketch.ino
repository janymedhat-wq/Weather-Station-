#include <DHT.h>
#include <Adafruit_Sensor.h>  // Required for DHT library

#define DHTPIN 2       // Digital pin connected to the DHT22
#define DHTTYPE DHT22  // Change to DHT11 if using that sensor

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);  // Start serial communication
  dht.begin();         // Initialize the DHT sensor
}

void loop() {
  float temp = dht.readTemperature(); // Celsius
  float hum = dht.readHumidity();     // Humidity %

  // Check if any reading failed
  if (isnan(temp) || isnan(hum)) {
    Serial.println("Error reading sensor!");
  } else {
    // Send data in CSV format for Python
    Serial.print(temp);
    Serial.print(",");
    Serial.println(hum);
  }

  delay(2000); // Read every 2 seconds
}
