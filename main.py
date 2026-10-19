# Waterfall Controller - ESP32 Version
# Direct port of Raspberry Pi logic
# Copyright Jeffrey L. Goode

from machine import Pin
import time

# -----------------------------
# Pin Assignments (ESP32)
# -----------------------------

# Inputs
water_level_pin = Pin(26, Pin.IN, Pin.PULL_UP)   # Float switch
big_fall_pin    = Pin(14, Pin.IN, Pin.PULL_UP)   # Big waterfall switch
little_fall_pin = Pin(27, Pin.IN, Pin.PULL_UP)   # Little waterfall switch

# Outputs (relays - ACTIVE HIGH on OONO F-1002)
big_pump_pin    = Pin(2, Pin.OUT)   # Relay 1
little_pump_pin = Pin(4, Pin.OUT)   # Relay 2
water_valve_pin = Pin(5, Pin.OUT)   # Relay 3

# Initialize relays OFF (LOW = off for active-high relay boards)
big_pump_pin.value(0)
little_pump_pin.value(0)
water_valve_pin.value(0)

# -----------------------------
# Main Loop
# -----------------------------
while True:

    # Read float (0 = low water, 1 = good water)
    water_level = water_level_pin.value()

    # Switches wired to GND:
    #   0 = ON (switch closed)
    #   1 = OFF (switch open)
    big_fall    = (big_fall_pin.value() == 0)
    little_fall = (little_fall_pin.value() == 0)

    # --- MASTER SAFETY RULE ---
    # If both switches are OFF, everything must be OFF regardless of float state.
    if not big_fall and not little_fall:
        big_pump_pin.value(0)      # OFF
        little_pump_pin.value(0)   # OFF
        water_valve_pin.value(0)   # OFF
        print("Both switches OFF — system disarmed.")
        time.sleep(1)
        continue

    # If water is low AND a waterfall is requested
    if (water_level == 0) and (big_fall or little_fall):
        water_valve_pin.value(1)   # turn valve ON (active high)

        # Turn pumps OFF while filling
        little_pump_pin.value(0)
        big_pump_pin.value(0)

        # Delay (shortened to 60 sec per your Pi code)
        time.sleep(60)

    else:
        water_valve_pin.value(0)   # turn valve OFF

    # Re-read water level after fill cycle
    water_level = water_level_pin.value()

    # Big waterfall pump logic (relay active-high)
    if water_level == 1 and big_fall:
        big_pump_pin.value(1)   # ON
    else:
        big_pump_pin.value(0)   # OFF

    # Little waterfall pump logic (relay active-high)
    if water_level == 1 and little_fall:
        little_pump_pin.value(1)   # ON
    else:
        little_pump_pin.value(0)   # OFF

    # Debug output
    print("water level =", water_level)
    print("little fall switch =", little_fall)
    print("big fall switch =", big_fall)
    print("water valve =", water_valve_pin.value(),
          "little pump =", little_pump_pin.value(),
          "big pump =", big_pump_pin.value())
    print()

    time.sleep(1)
