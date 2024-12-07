#include <LiquidCrystal_I2C.h>

void initializeLCD(LiquidCrystal_I2C &lcd) {
  lcd.init();
  lcd.backlight();
  lcd.clear();
  lcd.setCursor(1, 0);
  lcd.print("Gym Attendance");
  lcd.setCursor(2, 6);
  lcd.print("System");
  delay(2000);
  lcd.clear();
  lcd.print("Scan your card");
}

void displayValidUser(LiquidCrystal_I2C lcd, String firstName, int attendances) {
  lcd.clear();
  lcd.print("Welcome ");
  lcd.print(firstName);
  lcd.print("!");
  lcd.setCursor(0, 1);
  lcd.print(attendances);
  lcd.print(" attendances");
}

void displayInvalidUser(LiquidCrystal_I2C lcd) {
  lcd.clear();
  lcd.print("Access denied");
}

void displayNotRegisteredUser(LiquidCrystal_I2C lcd) {
  lcd.clear();
  lcd.print("Not registered!");
  lcd.setCursor(0,1);
  lcd.print("Registering...");
}

void displayRegistered(LiquidCrystal_I2C lcd) {
  lcd.clear();
  lcd.print("Registered!");
  delay(3000);
}

void displayScanCard(LiquidCrystal_I2C lcd) {
  lcd.clear();
  lcd.print("Scan your card");
}
