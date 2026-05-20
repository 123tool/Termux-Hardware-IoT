import os
import sys
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# Cari port USB Serial di Android/Termux
SERIAL_PORTS = ['/dev/ttyUSB0', '/dev/ttyACM0', '/dev/ttyUSB1', 'COM3'] # COM3 untuk testing di Windows
ser = None

# Coba inisialisasi koneksi hardware asli
for port in SERIAL_PORTS:
  try:
    import serial
    ser = serial.Serial(port, 115200, timeout=0.5)
    print(f"[+] Hardware Terdeteksi! Terhubung ke {port}")
    break
  except Exception:
    continue

# Fallback ke Emulator jika hardware tidak ditemukan
if ser is None:
  print("[!] Hardware asli tidak terdeteksi. Mengaktifkan Mode Simulator MockSerial...")
  from mock_serial import MockSerial
  ser = MockSerial('VIRTUAL_PORT_OTG', 115200)

# Penyimpan status terakhir kondisi smart home di memori server
device_states = {
  "lamp1": "OFF",
  "lamp2": "OFF",
  "ac": "OFF"
}

telemetry_data = {
  "temperature": "0",
  "light_level": "0",
  "voltage": "0.0"
}

def parse_telemetry():
  """Membaca data buffer serial dan memperbarui data sensor"""
  global telemetry_data
  try:
    # Membaca data jika tersedia
    if hasattr(ser, 'in_waiting') and ser.in_waiting == 0:
      return
      
    raw_line = ser.readline().decode('utf-8', errors='ignore').strip()
    if raw_line.startswith("TELEMETRY:"):
      # Contoh: TELEMETRY:TEMP=26|LIGHT=512|VOLT=220.5
      data_part = raw_line.replace("TELEMETRY:", "")
      pairs = data_part.split("|")
      for pair in pairs:
        if "=" in pair:
          k, v = pair.split("=")
          if k == "TEMP": telemetry_data["temperature"] = v
          if k == "LIGHT": telemetry_data["light_level"] = v
          if k == "VOLT": telemetry_data["voltage"] = v
  except Exception as e:
    print(f"Error parsing serial line: {e}")

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/api/status', methods=['GET'])
def get_status():
  """Endpoint berkala (polling) untuk mengambil telemetri sensor & status saklar"""
  parse_telemetry() # Update data sensor terbaru dari serial line
  return jsonify({
    "devices": device_states,
    "sensors": telemetry_data,
    "connection_type": "EMULATOR_MODE" if 'MockSerial' in str(type(ser)) else "HARDWARE_OTG_CONNECTED"
  })

@app.route('/api/control', methods=['POST'])
def control_device():
  """Endpoint untuk mengontrol on/off relay smart home"""
  global device_states
  payload = request.json or {}
  device = payload.get("device") # lamp1, lamp2, ac
  action = payload.get("action") # ON, OFF
  
  if device not in device_states or action not in ["ON", "OFF"]:
    return jsonify({"status": "error", "message": "Instruksi tidak dikenal!"}), 400
    
  # Susun string perintah serial sesuai kesepakatan dengan Arduino sketch
  serial_cmd = f"{device.upper()}_{action}\n"
  
  try:
    ser.write(serial_cmd.encode()) # Kirim instruksi biner lewat kabel OTG
    device_states[device] = action # Update status memori lokal server
    return jsonify({"status": "success", "device": device, "current_state": action})
  except Exception as e:
    return jsonify({"status": "error", "message": f"Gagal kirim ke hardware: {str(e)}"}), 500

if __name__ == '__main__':
  print("======================================================")
  print("   SPY-E // 123TOOL SMART HOME ENGINE SIAP BERAKSI     ")
  print("   Akses dashboard via browser HP: http://127.0.0.1:8080")
  print("======================================================")
  app.run(host='0.0.0.0', port=8080, debug=True)
