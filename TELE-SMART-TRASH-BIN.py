import network
import urequests
from time import sleep


SSID = 'Perpustakaan'
PASSWORD = 'maalmajaya'


BOT_TOKEN = '7711476454:AAH0yRuLwVnVUqsMqzl6XctVA4ayTqC9Ya0'  
CHAT_ID = '6110818464'  


def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    print("Menyambungkan ke WiFi...")
    while not wlan.isconnected():
        sleep(1)
    print("Terhubung ke WiFi:", wlan.ifconfig())


def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message
    }
    try:
        response = urequests.post(url, json=payload)
        print("Pesan berhasil dikirim ke Telegram.")
        response.close()
    except Exception as e:
        print("Gagal mengirim pesan:", e)


connect_wifi()
send_telegram_message("🚨 Tempat sampah penuh! Segera dikosongkan.")
