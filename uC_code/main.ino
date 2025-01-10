#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <LiquidCrystal_I2C.h>
#include <MFRC522.h>

#include "lcd.h"
#include "wifi.h"
#include "rfid.h"
#include "rgb.h"
#include "buzzer.h"

// AWS IoT MQTT Broker
const char *mqtt_broker = "a3lnnu1armgvqt-ats.iot.us-east-1.amazonaws.com";  // Your correct endpoint
const int mqtt_port = 8883;                                                  // Secure port for MQTT with TLS

// MQTT Topics
const char *check_user_topic = "/check_user";      // Replace with your publish topic
const char *user_details_topic = "/user_details";  // Replace with your response topic
const char *gym_status_topic = "/gym_status";      // Replace with your subscribe topic

// Certificates
const char *ca_cert =
  "-----BEGIN CERTIFICATE-----\n"
  "-----END CERTIFICATE-----\n";


const char *client_cert =
  "-----BEGIN CERTIFICATE-----\n"
  "-----END CERTIFICATE-----\n";

const char *private_key =
  "-----BEGIN RSA PRIVATE KEY-----\n"
  "-----END RSA PRIVATE KEY-----\n";

// Pins for peripherals
const int RFID_SS_PIN = 5;
const int RFID_RST_PIN = 0;

#define PIN_RED 33
#define PIN_GREEN 32
#define PIN_BUZZER 27

LiquidCrystal_I2C lcd(0x3F, 16, 2);
MFRC522 rfid(RFID_SS_PIN, RFID_RST_PIN);
WiFiClientSecure wifiClient;
PubSubClient mqttClient(wifiClient);

// Global variables
bool mqttResponseReceived = false;
String mqttResponse = "";
bool gymStatus = false; // false for gym open, true for gym closed

void mqttCallback(char *topic, byte *payload, unsigned int length) {
  char message[length + 1];
  memcpy(message, payload, length);
  message[length] = '\0';

  mqttResponse = String(message);
  mqttResponseReceived = true;

  if(strcmp(topic, gym_status_topic) == 0) {
    // Parse response
    StaticJsonDocument<200> responseDoc;
    deserializeJson(responseDoc, mqttResponse);

    gymStatus = responseDoc["gym_status"];
    if(gymStatus == true) {
      closeGym();
    } else {
      openGym();
    }

    mqttResponseReceived = false;
  }

  Serial.print("Message received on topic ");
  Serial.print(topic);
  Serial.print(": ");
  Serial.println(message);
}

void connectToMQTT() {
  while (!mqttClient.connected()) {
    Serial.println("Connecting to AWS IoT MQTT broker...");
    if (mqttClient.connect("ESP")) {
      Serial.println("Connected to AWS IoT!");
      mqttClient.subscribe(user_details_topic);
      mqttClient.subscribe(gym_status_topic);
    } else {
      Serial.print("Connection failed, rc=");
      Serial.println(mqttClient.state());
      delay(2000);
    }
  }
}

void setup() {
  Serial.begin(9600);

  connectToWiFi();
  initializeRFID(rfid);
  initializeRGB(PIN_RED, PIN_GREEN);
  initializeBuzzer(PIN_BUZZER);
  initializeLCD(lcd);

  // Configure MQTT
  wifiClient.setCACert(ca_cert);
  wifiClient.setCertificate(client_cert);
  wifiClient.setPrivateKey(private_key);

  mqttClient.setServer(mqtt_broker, mqtt_port);
  mqttClient.setCallback(mqttCallback);
  mqttClient.setKeepAlive(6000000000);

  connectToMQTT();
}

void loop() {
  // Maintain MQTT connection
  if (!mqttClient.connected()) {
    connectToMQTT();
  }
  mqttClient.loop();

  if(gymStatus == true) return; // if the gym is closed don't read cards

  // Reset the loop if no new card present on the sensor/reader
  if (!rfid.PICC_IsNewCardPresent())
    return;

  // Verify if the ID has been read
  if (!rfid.PICC_ReadCardSerial())
    return;

  String cardID = "";
  bool validCard = getCardID(rfid, cardID);
  if (!validCard)
    return;

  Serial.print("Card ID is ");
  Serial.println(cardID);

  // Publish card ID to MQTT broker
  StaticJsonDocument<200> doc;
  doc["card_id"] = cardID;
  String message;
  serializeJson(doc, message);

  Serial.println("Publishing card ID to MQTT...");
  mqttClient.publish(check_user_topic, message.c_str());

  // Wait for a response from the server
  unsigned long startTime = millis();
  mqttResponseReceived = false;
  while (!mqttResponseReceived && millis() - startTime < 10000) {
    mqttClient.loop();
  }

  if (mqttResponseReceived) {
    mqttResponseReceived = false;

    // Parse response
    StaticJsonDocument<200> responseDoc;
    deserializeJson(responseDoc, mqttResponse);

    String membershipStatus = responseDoc["status"];
    if (membershipStatus == "valid") {
      String firstName = responseDoc["first_name"];
      int attendances = responseDoc["attendances"];
      validUser(firstName, attendances);
    } else if (membershipStatus == "invalid") {
      invalidUser();
    } else if (membershipStatus == "not registered") {
      notRegisteredUser();

        unsigned long startTime = millis();
      while (!mqttResponseReceived && millis() - startTime < 120000) {
        mqttClient.loop();
      }

      if (mqttResponseReceived) {
        Serial.print("User was registered. Parsing its data...\n");
        mqttResponseReceived = false;

        // Parse response
        StaticJsonDocument<200> responseDoc;
        deserializeJson(responseDoc, mqttResponse);

        String membershipStatus = responseDoc["status"];
        if (membershipStatus == "valid") {
          String firstName = responseDoc["first_name"];
          int attendances = responseDoc["attendances"];
          validUser(firstName, attendances);
        } else if (membershipStatus == "invalid") {
          invalidUser();
        }
      }
    }
  } else {
    Serial.println("No response received from server.");
  }

  delay(3000); 

  // Go back to default state
  noColorRGB(PIN_RED, PIN_GREEN);
  displayScanCard(lcd);

  stopRFID(rfid);
}

void validUser(String firstName, int attendances) {
  Serial.print("User is registered and valid\n");
  displayValidUser(lcd, firstName, attendances);
  greenRGB(PIN_RED, PIN_GREEN);
  validUserBuzzer(PIN_BUZZER);
}

void invalidUser() {
  Serial.print("User is registered and invalid\n");
  displayInvalidUser(lcd);
  redRGB(PIN_RED, PIN_GREEN);
  invalidUserBuzzer(PIN_BUZZER);
}

void notRegisteredUser() {
  Serial.print("User is not registered\n");
  displayNotRegisteredUser(lcd);
  orangeRGB(PIN_RED, PIN_GREEN);
}

void closeGym() {
  Serial.print("Gym is closed\n");
  displayGymClosed(lcd);
  redRGB(PIN_RED, PIN_GREEN);
}

void openGym() {
  Serial.print("Gym is open\n");
  greenRGB(PIN_RED, PIN_GREEN);
  displayGymOpen(lcd);
  delay(500);
  noColorRGB(PIN_RED, PIN_GREEN);
}
