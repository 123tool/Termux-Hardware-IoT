## Termux.Hardware-IoT

`Termux.Hardware-IoT` adalah platform kontrol perangkat elektronik dan otomasi rumah (*Smart Home*) berbasis web yang dieksekusi langsung dari dalam ekosistem Android menggunakan Termux. Platform ini memanfaatkan jalur komunikasi **Serial Bus (USB OTG)** secara lokal, menjadikannya solusi kontrol perangkat keras yang mandiri, berlatensi rendah, dan beroperasi penuh tanpa ketergantungan pada koneksi internet ataupun broker MQTT eksternal.

Proyek ini dilengkapi dengan fitur **Auto-Fallback Simulator Engine** (Mock Serial). Jika hardware asli tidak terdeteksi, server otomatis beralih ke mode simulasi, memungkinkan pengujian performa UI/UX tetap berjalan lancar selama proses pengembangan.

---

## Fitur

* **Direct USB OTG Serial Driver:** Komunikasi dua arah (*duplex*) berkecepatan tinggi (115200 bps) langsung ke modul mikrokontroler (Arduino/ESP32) tanpa proses root Android.
* **Real-Time Telemetry Polling:** Sinkronisasi asinkronus otomatis setiap 1 detik untuk memperbarui metrik sensor (Suhu, Intensitas Cahaya LDR, dan Voltase Jaringan) langsung ke UI tanpa interupsi muat ulang (*reload*) halaman.
* **Auto-Fallback Simulator:** Sistem cerdas mendeteksi ketersediaan port `/dev/ttyUSB*` atau `/dev/ttyACM*`. Jika hardware dicabut, simulator data sensor akan mengambil alih secara otomatis agar server tidak *crash*.

---

## Instalasi & Setup
​1. Tahap Persiapan Hardware (Arduino Side)
​Buka berkas arduino_sketch/arduino_sketch.ino menggunakan Arduino IDE di PC/Laptop Anda.
​Sambungkan papan pengontrol Anda (Arduino Uno/Nano/Mega atau ESP32).
​Lakukan kompilasi (Compile) dan unggah (Upload) program tersebut ke papan pengontrol hingga selesai.
​2. Persiapan Lingkungan Android (Termux Side)
​Buka aplikasi Termux di ponsel Android Anda, kemudian jalankan serangkaian perintah berikut untuk memperbarui sistem dan memasang dependensi inti :

## Indeks paket Termux
```
pkg update && pkg upgrade -y
```
## Instal Python dan Git
```
pkg install python git -y
```
## Pustaka Flask dan PySerial
```
pip install flask pyserial
```
## Clone Repositori
```
git clone https://github.com/123tool/Termux-Hardware-IoT.git
cd Termux-Hardware-IoT
```
## Menjalankan & Pengoperasian

- ​Langkah 1 :
Penyambungan Kabel OTG Fisik
​Hubungkan papan Arduino/ESP32 ke ponsel Android Anda menggunakan kabel data USB yang disambungkan ke adapter USB OTG.
​Ketika muncul pop-up notifikasi di Android yang menanyakan izin akses perangkat USB ke Termux, berikan centang Izinkan/OK.

- Langkah 2 :
Eksekusi Server Utama
​Jalankan mesin backend dengan mengetik perintah berikut di dalam direktori proyek Termux Anda :
```
python3 app.py
```
Sistem akan membaca jalur hardware Anda. Perhatikan indikator log pada terminal :
​- Jika Hardware Terhubung: [+] Hardware Terdeteksi! Terhubung ke /dev/ttyUSB0
- ​Jika Menggunakan Mode Simulasi: [!] Hardware asli tidak terdeteksi. Mengaktifkan Mode Simulator MockSerial...

## ​Langkah 3 :
Akses Dashboard via Browser Ponsel
Buka browser di ponsel Android Anda (Google Chrome, Kiwi Browser, atau Firefox).
Ketik alamat URL lokal berikut pada kolom navigasi browser :
```
http://127.0.0.1:8080
```
