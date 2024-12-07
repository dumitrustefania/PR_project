void initializeRGB(int PIN_RED, int PIN_GREEN) {
  pinMode(PIN_RED, OUTPUT);
  pinMode(PIN_GREEN, OUTPUT);
}

void redRGB(int PIN_RED, int PIN_GREEN) {
  analogWrite(PIN_RED,   255);
  analogWrite(PIN_GREEN, 0);
}

void greenRGB(int PIN_RED, int PIN_GREEN) {
  analogWrite(PIN_RED,   0);
  analogWrite(PIN_GREEN, 255);
}

void orangeRGB(int PIN_RED, int PIN_GREEN) {
  analogWrite(PIN_RED,   255);
  analogWrite(PIN_GREEN, 120);
}

void noColorRGB(int PIN_RED, int PIN_GREEN) {
  analogWrite(PIN_RED,   0);
  analogWrite(PIN_GREEN, 0);
}
