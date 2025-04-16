import network
import time
from machine import Pin, time_pulse_us
import urequests

WIFI_SSID = 'Perpustakaan'
WIFI_PASS = 'maalmajaya'

UBIDOTS_TOKEN = 'BBUS-RP0OHVhu4wjCztt03F8vCDvxMIfzpz'
UBIDOTS_DEVICE = 'rpl-8'
UBIDOTS_VARIABLE = 'JARAK-SAMPAH'

TRIG_PIN = 5
ECHO_PIN = 18
LED_PIN = 2

trig = Pin(TRIG_PIN, Pin.OUT)
echo = Pin(ECHO_PIN, Pin.IN)
led = Pin(LED_PIN, Pin.OUT)

def connect_wifi():
    print("Menyambungkan ke Wi-Fi...")
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASS)
    while not wlan.isconnected():
        print(".", end="")
        time.sleep(0.5)
    print("\nTerhubung dengan IP:", wlan.ifconfig()[0])

def get_distance():
    trig.off()
    time.sleep_us(2)
    trig.on()
    time.sleep_us(10)
    trig.off()

    try:
        duration = time_pulse_us(echo, 1, 30000)  # timeout 30 ms
        distance = (duration / 2) / 29.1  # dalam cm
        return round(distance, 2)
    except OSError:
        return None

def send_to_ubidots(distance):
    url = f"http://industrial.api.ubidots.com/api/v1.6/devices/{UBIDOTS_DEVICE}/"
    headers = {
        "X-Auth-Token": UBIDOTS_TOKEN,
        "Content-Type": "application/json"
    }
    data = {UBIDOTS_VARIABLE: distance}
    try:
        response = urequests.post(url, json=data, headers=headers)
        print("Data terkirim:", response.text)
        response.close()
    except Exception as e:
        print("Gagal mengirim:", e)

connect_wifi()

while True:
    jarak_cm = get_distance()
    if jarak_cm is not None:
        print("Jarak:", jarak_cm, "cm")

        if jarak_cm <= 15:
            led.on()
        else:
            led.off()

        send_to_ubidots(jarak_cm)
    else:
        print("Gagal membaca jarak")

    time.sleep(5)
