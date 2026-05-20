## Termux.Hardware-IoT

`Termux.Hardware-IoT` adalah platform kontrol perangkat elektronik dan otomasi rumah (*Smart Home*) berbasis web yang dieksekusi langsung dari dalam ekosistem Android menggunakan Termux. Platform ini memanfaatkan jalur komunikasi **Serial Bus (USB OTG)** secara lokal, menjadikannya solusi kontrol perangkat keras yang mandiri, berlatensi rendah, dan beroperasi penuh tanpa ketergantungan pada koneksi internet ataupun broker MQTT eksternal.

Proyek ini dilengkapi dengan fitur **Auto-Fallback Simulator Engine** (Mock Serial). Jika hardware asli tidak terdeteksi, server otomatis beralih ke mode simulasi, memungkinkan pengujian performa UI/UX tetap berjalan lancar selama proses pengembangan.

---

## Fitur

* **Direct USB OTG Serial Driver:** Komunikasi dua arah (*duplex*) berkecepatan tinggi (115200 bps) langsung ke modul mikrokontroler (Arduino/ESP32) tanpa proses root Android.
* **Real-Time Telemetry Polling:** Sinkronisasi asinkronus otomatis setiap 1 detik untuk memperbarui metrik sensor (Suhu, Intensitas Cahaya LDR, dan Voltase Jaringan) langsung ke UI tanpa interupsi muat ulang (*reload*) halaman.
* **Industrial Neo-Brutalism Dark UI:** Desain antarmuka berwajah cyberpunk gelap dengan komponen sakelar (*toggle*) berukuran besar yang responsif dan sangat nyaman diakses via jempol ponsel.
* **Auto-Fallback Simulator:** Sistem cerdas mendeteksi ketersediaan port `/dev/ttyUSB*` atau `/dev/ttyACM*`. Jika hardware dicabut, simulator data sensor akan mengambil alih secara otomatis agar server tidak *crash*.

---
