# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)

import network
import time

SSID = "MY SSID"
PASSWORD = "MY Password"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

wlan.ifconfig((
    "192.168.4.50",
    "255.255.255.0",
    "192.168.4.1",
    "8.8.8.8"
))

print("Connecting to WiFi...")

wlan.connect(SSID, PASSWORD)

timeout = 20

while not wlan.isconnected() and timeout > 0:
    time.sleep(1)
    timeout -= 1

if wlan.isconnected():
    print("WiFi connected")
    print("IP Address:", wlan.ifconfig()[0])
    print("Network:", wlan.ifconfig())

    import webrepl
    webrepl.start()

else:
    print("WiFi connection failed")