// arduino_sketch.ino
// Driver Kontrol Rumah SPY-E & 123Tool

#define RELAY_LAMPU_1 2
#define RELAY_LAMPU_2 3
#define RELAY_AC      4

unsigned long lastSignalTime = 0;

void setup() {
  Serial.begin(115200); // Kecepatan tinggi untuk performa responsif
  
  pinMode(RELAY_LAMPU_1, OUTPUT);
  pinMode(RELAY_LAMPU_2, OUTPUT);
  pinMode(RELAY_AC, OUTPUT);
  
  // Default: Matikan semua relay (Active LOW biasanya pada modul relay)
  digitalWrite(RELAY_LAMPU_1, HIGH);
  digitalWrite(RELAY_LAMPU_2, HIGH);
  digitalWrite(RELAY_AC, HIGH);
}

void loop() {
  // 1. Baca Perintah Masuk dari Termux via Serial
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    
    if (command == "LAMP1_ON")  digitalWrite(RELAY_LAMPU_1, LOW);
    if (command == "LAMP1_OFF") digitalWrite(RELAY_LAMPU_1, HIGH);
    if (command == "LAMP2_ON")  digitalWrite(RELAY_LAMPU_2, LOW);
    if (command == "LAMP2_OFF") digitalWrite(RELAY_LAMPU_2, HIGH);
    if (command == "AC_ON")     digitalWrite(RELAY_AC, LOW);
    if (command == "AC_OFF")    digitalWrite(RELAY_AC, HIGH);
  }
  
  // 2. Kirim Telemetri Data Sensor ke Termux setiap 2 detik secara Otomatis
  if (millis() - lastSignalTime >= 2000) {
    lastSignalTime = millis();
    
    // Simulasi sensor internal (ganti dengan analogRead sensor asli jika ada)
    int LDR_Value = analogRead(A0); 
    float voltase = (analogRead(A1) * 5.0) / 1024.0 * 5.0; // Simulasi sensor tegangan
    int suhu = random(24, 29); // Simulasi sensor suhu DHT
    
    // Format pengiriman data yang mudah diparsing oleh Python backend
    Serial.print("TELEMETRY:");
    Serial.print("TEMP="); Serial.print(suhu); Serial.print("|");
    Serial.print("LIGHT="); Serial.print(LDR_Value); Serial.print("|");
    Serial.print("VOLT="); Serial.println(voltase);
  }
}
