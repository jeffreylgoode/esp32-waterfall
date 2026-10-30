# Waterfall Controller - ESP32 Version
# Direct port of Raspberry Pi logic
# Copyright Jeffrey L. Goode

VERSION = "2.24"

print()
print("Waterfall Controller")
print("Version:", VERSION)
print()

from machine import Pin
import time

# -----------------------------
# Pin Assignments (ESP32)
# -----------------------------

# Float switch
water_level_pin = Pin(26, Pin.IN, Pin.PULL_UP)

# New floats for highest float, and lowest float
# Highest float is another check to see if water is overflowing the pond
# Lowest float is a check to see if water level is nearing dangerous level for the big pump

high_float_pin = Pin(25, Pin.IN, Pin.PULL_UP)
low_float_pin = Pin(33, Pin.IN, Pin.PULL_UP)

# Switches - the inputs are active low since the switch ON causes a logic 0 

# Top switch = Little Falls
big_fall_pin = Pin(27, Pin.IN, Pin.PULL_UP)

# Bottom switch = Big Falls
little_fall_pin = Pin(14, Pin.IN, Pin.PULL_UP)

# Outputs (ACTIVE HIGH)

# Top outlet = Little Pump
little_pump_pin = Pin(4, Pin.OUT)

# Bottom outlet = Big Pump
big_pump_pin = Pin(2, Pin.OUT)

# Fill valve
water_valve_pin = Pin(5, Pin.OUT)

# Initialize outputs OFF
little_pump_pin.value(0)
big_pump_pin.value(0)
water_valve_pin.value(0)

# Fault logic variable - if the water level float has failed, one or two may happen
# the big pump may run dry, so let's cause a fault if we ever see the low level float see water low
# or and, if we ever see the pond overflow, we will also cause this to be a fault

fault_latched = False
fault_reason = ""

# -----------------------------
# Main Loop
# -----------------------------

while True:

    if fault_latched:

        little_pump_pin.value(0)
        big_pump_pin.value(0)
        water_valve_pin.value(0)

        print("FAULT LATCHED")
        print("REASON:", fault_reason)
        print("Set BOTH switches OFF to clear")
        #read switches
        little_fall = (little_fall_pin.value() == 0)
        big_fall = (big_fall_pin.value() == 0)
        # until both switches are set to OFF, the fault will remain
        
        if not little_fall and not big_fall:
            print("Fault cleared")
            fault_reason = ""
            fault_latched = False

        time.sleep(1)
        continue

    # Float switch
    # 0 = low water
    # 1 = water OK
    water_level = water_level_pin.value()
    
    # new floats
    # low_level = 1 is good, that means low float sees water
    # high_level = 0 is good, that means high float does not see water, and that pond is not overflowing
    # if low_level = 0, this is actually catestrophic meaning the big pump is about to run dry
    # if high_level = 1, this means the pond has overflowed


    high_level = high_float_pin.value()
    low_level = low_float_pin.value()
    print("high_level value", high_level)
    print("low_level value", low_level)
    print()
    big_pump_is_dry = (low_level == 0)
    pond_has_overflowed = (high_level == 1)
    print("big pump is dry", big_pump_is_dry)
    print("pond has overflowed", pond_has_overflowed)
    print()
    
    # Active LOW switches
    # 0 = switch ON
    # 1 = switch OFF
    # 0 = switch on causes the if equal 0 to be True
    little_fall = (little_fall_pin.value() == 0)
    big_fall = (big_fall_pin.value() == 0)
    
    print("top switch (little falls)", little_fall)
    print("bottom switch (big falls)", big_fall)
    print("little_fall_pin value", little_fall_pin.value())
    print("big_fall_pin value", big_fall_pin.value())
    print()
    print("little_fall_pin value", little_fall_pin.value())
    print("big_fall_pin value", big_fall_pin.value())
    
    # -------------------------
    # Don't operate the waterfalls if the switches are not active
    # -------------------------
    if not little_fall and not big_fall:

        little_pump_pin.value(0)
        big_pump_pin.value(0)
        water_valve_pin.value(0)

        print("Both switches are OFF - system disarmed.")
 
        time.sleep(1)
        continue

    # -------------------------
    # Turn off both pumps and water if the big pump is about to run dry
    # Turn off both pumps and water if pond has overflowed 
    # -------------------------
    if big_pump_is_dry:
        
        little_pump_pin.value(0)
        big_pump_pin.value(0)
        water_valve_pin.value(0)

        fault_latched = True
        print("FAULT: Big pump is about to run dry")
        fault_reason = "BIG PUMP DRY"
        time.sleep(1)
        continue

    # -------------------------
    # Turn off both pumps and water if pond has overflowed 
    # -------------------------
    if pond_has_overflowed:
        little_pump_pin.value(0)
        big_pump_pin.value(0)
        water_valve_pin.value(0)

        fault_latched = True
        print("FAULT: Pond has overflowed")
        fault_reason = "POND OVERFLOW"
        time.sleep(1)
        continue

    # -------------------------
    # Fill Cycle
    # -------------------------
    if water_level == 0 and (little_fall or big_fall):

        water_valve_pin.value(1)

        little_pump_pin.value(0)
        big_pump_pin.value(0)

        time.sleep(60)

    else:
        water_valve_pin.value(0)

    # Re-read level after fill cycle
    water_level = water_level_pin.value()

    # -------------------------
    # Little Falls
    # -------------------------
    if water_level == 1 and little_fall:
        little_pump_pin.value(1)
    else:
        little_pump_pin.value(0)

    # -------------------------
    # Big Falls
    # -------------------------
    if water_level == 1 and big_fall:
        big_pump_pin.value(1)
    else:
        big_pump_pin.value(0)

    # -------------------------
    # Debug Output
    # -------------------------
    print("water level =", water_level)
    print("little fall switch =", little_fall)
    print("big fall switch =", big_fall)
    

    print(
        "water valve =", water_valve_pin.value(),
        "little pump =", little_pump_pin.value(),
        "big pump =", big_pump_pin.value()
    )
    



    print()

    time.sleep(1)

