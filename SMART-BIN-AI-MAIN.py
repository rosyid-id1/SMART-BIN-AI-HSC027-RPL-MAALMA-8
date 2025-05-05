import network
import time
from machine import Pin, time_pulse_us, PWM
import urequests

WIFI_SSID = 'RPL'
WIFI_PASS = 'maalmajaya'
UBIDOTS_TOKEN = 'BBUS-RP0OHVhu4wjCztt03F8vCDvxMIfzpz'
UBIDOTS_DEVICE = 'rpl-8'
UBIDOTS_VARIABLE = 'JARAK-SAMPAH'

TRIG1 = Pin(2, Pin.OUT)  
ECHO1 = Pin(4, Pin.IN)

TRIG2 = Pin(12, Pin.OUT)  
ECHO2 = Pin(13, Pin.IN)

servo = PWM(Pin(15), freq=50) 
led = Pin(5, Pin.OUT)         

def connect_wifi():
    print("Menyambungkan ke Wi-Fi...")
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASS)
    retries = 0
    while not wlan.isconnected() and retries < 20:
        print(".", end="")
        time.sleep(0.5)
        retries += 1
    if wlan.isconnected():
        print("\nTerhubung dengan IP:", wlan.ifconfig()[0])
    else:
        print("\nGagal terhubung ke Wi-Fi setelah 20 percobaan.")

def get_distance(trig, echo):
    trig.off()
    time.sleep_us(2)
    trig.on()
    time.sleep_us(10)
    trig.off()

    try:
        duration = time_pulse_us(echo, 1, 30000)
        distance = (duration / 2) / 29.1
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
        if response.status_code == 200:
            print("Data terkirim:", response.text)
        else:
            print("Gagal mengirim data:", response.status_code, response.text)
        response.close()
    except Exception as e:
        print("Gagal mengirim:", e)

def set_servo_angle(angle):
    duty = int((angle / 180) * 75) + 40
    servo.duty(duty)

connect_wifi()

while True:
    # --- Sensor 1: kontrol SERVO
    jarak_servo = get_distance(TRIG1, ECHO1)
    if jarak_servo is not None:
        print("[Sensor 1 - Servo] Jarak:", jarak_servo, "cm")
        if jarak_servo >= 10:
            set_servo_angle(140)
        else:
            set_servo_angle(0)
    else:
        print("[Sensor 1 - Servo] Gagal membaca jarak.")

    # --- Sensor 2: kontrol LED + kirim Ubidots
    jarak_led = get_distance(TRIG2, ECHO2)
    if jarak_led is not None:
        print("[Sensor 2 - LED] Jarak:", jarak_led, "cm")
        if jarak_led >= 10:
            led.on()
        else:
            led.off()

        send_to_ubidots(jarak_led)
    else:
        print("[Sensor 2 - LED] Gagal membaca jarak.")

    time.sleep(2) 
