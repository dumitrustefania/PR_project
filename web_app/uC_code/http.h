#include <WiFi.h>
#include <HTTPClient.h>

const char *ssid = "SSID";
const char *password = "PASSWORD";
const char *serverAddress = "https://pr-project-f8c7fbee3ae5.herokuapp.com/api/check_user";

void connectToWiFi() {
  Serial.println("Connecting to WiFi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting...");
  }
  Serial.println("Connected to WiFi");
}

int sendPOSTRequest(HTTPClient &http, String cardID, bool firstRequest) {
  // Create JSON payload containing the card ID
  StaticJsonDocument<200> cardJson;
  cardJson["card_id"] = cardID;
  cardJson["first_request"] = true;
  String jsonPayload;
  serializeJson(cardJson, jsonPayload);

  http.addHeader("Content-Type", "application/json");
  return http.POST(jsonPayload);
}
