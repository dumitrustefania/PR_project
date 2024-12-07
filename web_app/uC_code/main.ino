#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <LiquidCrystal_I2C.h>
#include <MFRC522.h>

#include "lcd.h"
#include "http.h"
#include "rfid.h"
#include "rgb.h"
#include "buzzer.h"

const int RFID_SS_PIN = 5;
const int RFID_RST_PIN = 0;

#define PIN_RED 33
#define PIN_GREEN 32
#define PIN_BUZZER 27

LiquidCrystal_I2C lcd(0x3F, 16, 2);
MFRC522 rfid(RFID_SS_PIN, RFID_RST_PIN);

void setup() {
  Serial.begin(9600);
    
  connectToWiFi();
  initializeRFID(rfid);
  initializeRGB(PIN_RED, PIN_GREEN);
  initializeBuzzer(PIN_BUZZER);  
  initializeLCD(lcd);
}

void loop() {
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

  // Send request to server
  if (sendCheckUserRequest(cardID)) {
    // Delay to allow the user to read the output
    delay(3000); 

    // Go back to default state
    noColorRGB(PIN_RED, PIN_GREEN);
    displayScanCard(lcd);
  }

  stopRFID(rfid);
}

bool sendCheckUserRequest(String cardID) {
  HTTPClient http;

  Serial.println("Sending POST request to server...");
  if (http.begin(serverAddress)) {
    int httpResponseCode = sendPOSTRequest(http, cardID, true);

    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.print("Response Code: ");
      Serial.println(httpResponseCode);
      Serial.print("Response: ");
      Serial.println(response);

      DynamicJsonDocument doc(200);
      deserializeJson(doc, response);

      String membershipStatus = doc["status"];
      if (membershipStatus == "valid") {
        String firstName = doc["first_name"];
        int attendances = doc["attendances"];
        validUser(firstName, attendances);
      } else if (membershipStatus == "invalid") {
        invalidUser();
      } else if (membershipStatus == "not registered") {
        notRegisteredUser();

        // Perform long polling until the user is registered from the UI
        while (membershipStatus == "not registered") {
          delay(3000); // Delay to avoid flooding the server with requests
          Serial.println("Performing long polling...");
        
          int httpResponseCode = sendPOSTRequest(http, cardID, false);

          if (httpResponseCode > 0) {
            String response = http.getString();
            Serial.print("Response Code: ");
            Serial.println(httpResponseCode);
            Serial.print("Response: ");
            Serial.println(response);

            DynamicJsonDocument doc(200);
            deserializeJson(doc, response);
            membershipStatus = doc["status"].as<String>();

            if (membershipStatus == "valid") {
              String firstName = doc["first_name"];
              int attendances = doc["attendances"];
              displayRegistered(lcd);
              validUser(firstName, attendances);
            } else if (membershipStatus == "invalid") {
              displayRegistered(lcd);
              invalidUser();
            }
          } else {
            Serial.println("Error on HTTP request");
          }
        }
      }
      http.end();
      return true;
    } else {
      Serial.println("Error on HTTP request");
      http.end();
      return false;
    }
  } else {
    Serial.println("Unable to connect to server");
    return false;
  }
}

void validUser(String firstName, int attendances) {
  displayValidUser(lcd, firstName, attendances);
  greenRGB(PIN_RED, PIN_GREEN);
  validUserBuzzer(PIN_BUZZER);
}

void invalidUser() {
  displayInvalidUser(lcd);
  redRGB(PIN_RED, PIN_GREEN);
  invalidUserBuzzer(PIN_BUZZER);
}

void notRegisteredUser() {
  displayNotRegisteredUser(lcd);
  orangeRGB(PIN_RED, PIN_GREEN);
}
