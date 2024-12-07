void initializeBuzzer(int PIN_BUZZER) {
  pinMode(PIN_BUZZER, OUTPUT);
}

void validUserBuzzer(int PIN_BUZZER) {
  tone(PIN_BUZZER, 1000, 200);
  delay(100);
  tone(PIN_BUZZER, 1000, 200);
  delay(80);
  tone(PIN_BUZZER, 1500, 300);
}

void invalidUserBuzzer(int PIN_BUZZER) {
  tone(PIN_BUZZER, 350, 600);
}
