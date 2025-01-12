# Proiect PR-IoT

## Autor
Dumitru Bianca Ștefania

---

## Introducere
Proiectul își propune monitorizarea și gestionarea accesului într-o sală de sport. Sistemul permite verificarea abonamentului utilizatorilor și contorizarea prezențelor, cu o interfață web pentru administratori și feedback direct pentru utilizatori prin componente hardware interactive (LED RGB, LCD, buzzer).

### Funcționalități principale:
1. Verificare abonament și acces utilizatori.
2. Contorizare prezențe și afișare live pe interfața web.
3. Statistici detaliate și vizualizare prezențe individuale.
4. Înregistrarea automată a unui utilizator nou la scanarea cardului.
5. Control bidirecțional între interfața web și dispozitivul hardware.

---

## Structura Proiectului

### Directoare principale:
- **`uC_code/`**
  - Conține codul pentru ESP32, inclusiv inițializarea componentelor și logica principală a sistemului.
  - Structură: 
    - `main.ino` - Logica principală a dispozitivului.
    - Fișiere de inițializare: `wifi.h`, `lcd.h`, `rgb.h`, etc.

- **`gym-attendance-backend/`**
  - Backend implementat în Flask pentru gestionarea logicii serverului și comunicarea cu broker-ul MQTT.

- **`gym-attendance-frontend/`**
  - Interfața web React pentru administrarea utilizatorilor și vizualizarea statisticilor.
  - `src/` - Conține componente React (e.g., `Statistics.js`, `UserDetails.js`).

- **`Procfile`**,  **`deploy.sh`**,  **`package.json`**, etc.
  - Fișiere folosite pentru deployment-ul serverului pe platforma Heroku.
  - 
### Tehnologii utilizate:
- **Microcontroller:** ESP32 WROOM
- **Backend:** Flask
- **Frontend:** React
- **Protocol comunicație:** MQTT (cu AWS IoT Core ca broker)
- **Deploy backend:** Heroku

---

## Funcționare
1. **Scanarea cardului:**
   - Se verifică validitatea abonamentului prin comunicarea cu serverul.
   - Utilizatorii primesc feedback direct prin LED, LCD și buzzer.

2. **Interfața web:**
   - Statistici live despre prezențe.
   - Opțiuni de înregistrare și vizualizare detalii utilizatori.

3. **Control de la distanță:**
   - Administratorii pot controla starea sălii și dispozitivul hardware prin interfața web.

---

## Securitate
- Comunicația dintre dispozitiv, server și broker-ul MQTT este criptată și autentificată folosind protocolul TLS cu certificate AWS IoT Core.

---

## Concluzie
Proiectul demonstrează integrarea eficientă a componentelor hardware și software într-un sistem IoT complet funcțional. Următoarele îmbunătățiri ar putea include optimizări ale interfeței web și scalarea infrastructurii pentru utilizare reală.
