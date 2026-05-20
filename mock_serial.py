import random
import time

class MockSerial:
  def __init__(self, port, baudrate, timeout=1):
    self.port = port
    self.is_open = True
    print(f"[MOCK SERIAL] Terhubung secara virtual ke port {port} ({baudrate} bps)")

  def write(self, data):
    print(f"[MOCK SERIAL SEND] -> {data.decode().strip()}")

  def readline(self):
    time.sleep(0.5)
    # Membuat string telemetri tiruan mirip output Arduino asli
    suhu = random.randint(22, 31)
    cahaya = random.randint(200, 850)
    volt = round(random.uniform(210.5, 230.2), 1)
    return f"TELEMETRY:TEMP={suhu}|LIGHT={cahaya}|VOLT={volt}\n".encode()

  def close(self):
    self.is_open = False
