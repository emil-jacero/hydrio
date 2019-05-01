#! /bin/python3

import time
import asyncio
import random

## TODO: Get some feedback system to determine if pump is running


## Initiate Pins IN and Pins OUT
#s_1 = Pin('P9', Pin.IN, Pin.PULL_UP) # Sensor 1
#s_2 = Pin('P10', Pin.IN, Pin.PULL_UP) # Sensor 2
#relay_1 = Pin('P11', Pin.OUT)
#relay_2 = Pin('P12', Pin.OUT)

## Initiate relays in NO (Normally Opened) position
#relay_1.value(1)
#relay_2.value(1)


max_pump_time = 10 # The maximum amount of second to run the pump

class PumpObject:
    def __init__(self, name, location, gpio_pin):
        self.name = name
        self.location = location
        self.powered_state = False
        self.temprature = None
        self.relay = gpio_pin
        self.pump_start_time = None
        self.pump_stop_time = None

    def get_status(self):
        if self.powered_on is True:
            temporary_stop_time = time.time()
            print("INFO: Pump is running [Time running: {}s]".format(int(temporary_stop_time - self.pump_start_time)))
            return True
        else:
            print("INFO: Pump is powered off")
            return False

    def get_time_since_start(self):
        temporary_stop_time = time.time()
        print("INFO: Time since start: {}s]".format(int(temporary_stop_time - self.pump_start_time)))
        return temporary_stop_time - self.pump_start_time

    def start_pump(self):
        if self.powered_on is False:
            print("INFO: Attempting to start the pump")
            ## TODO: Run try function to initiate GPIO pin to start pump. Possible feedback?
            self.powered_on = True
            self.pump_start_time = time.time()
        else:
            temporary_stop_time = time.time()
            print("INFO: Pump is already running [Time running: {}]".format((temporary_stop_time - self.pump_start_time)))

    def stop_pump(self):
        if self.powered_on is True:
            print("INFO: Attempting to stop the pump")
            ## TODO: Run try function to initiate GPIO pin to stop pump. Possible feedback?
            self.powered_on = False
            self.pump_stop_time = time.time()
            print("INFO: Time running: {}".format((self.pump_stop_time - self.pump_start_time)))
        else:
            print("INFO: Pump already stopped")
            print("INFO: Time running: {}".format((self.pump_stop_time - self.pump_start_time)))


class PinObject:
    def __init__(self, pin_nr, pin_type, pin_state):
        self.pin_obj = None
        self.pin_nr = pin_nr  # Integer
        self.pin_type = pin_type  # IN or OUT
        self.pin_state = pin_state  # Only for IN (PULL_UP or PULL_DOWN)
        """
        if pin_type == 'IN':
            if pin_state == "PULL_UP":
                self.pin_obj = Pin(pin_nr, Pin.IN, Pin.PULL_UP)
            elif pin_state == "PULL_DOWN":
                self.pin_obj = Pin(pin_nr, Pin.IN, Pin.PULL_DOWN)
        elif pin_type == 'OUT':
            self.pin_obj = Pin(pin_nr, Pin.OUT)
            self.pin_obj.value(0)
        """


class SensorObject:
    def __init__(self, name, location, position, sensor_type, gpio_pin):
        self.name = name
        self.location = location  # In what region is it located
        self.position = position  # Where in that region is it located
        self.sensor_type = sensor_type  # Temperature, Pressure, Level
        self.sensor = gpio_pin
        self.value = None

    def pull_sensor(self):
        # self.value = self.sensor.value
        self.value = random.randint(0, 1)  # TESTING
        if self.value == 0:
            return False
        elif self.value == 1:
            return True


def pump_function():
    # Initialize all sensors (create as SensorObject)
    pin1 = PinObject(pin_nr=1, pin_type="IN", pin_state="PULL_UP")
    pin2 = PinObject(pin_nr=2, pin_type="IN", pin_state="PULL_UP")
    sens1 = SensorObject(name="sens1", location="well", position="Bottom", sensor_type="level", gpio_pin=pin1)
    sens2 = SensorObject(name="sens2", location="well", position="Top", sensor_type="level", gpio_pin=pin2)

    pin3 = PinObject(pin_nr=2, pin_type="OUT", pin_state=None)  # TODO: Fix so that no pin_state is required
    pump1 = PumpObject(name="pump1", location="well", gpio_pin=pin3)
    set_reset = False # Always set to False by default

    time_start = time.time()
    sens1.pull_sensor()
    sens2.pull_sensor()
    #print('{} {}-{} {}'.format(sens1.position, sens1.value, sens2.position, sens2.value))

    # If full
    if sens1.value == 1 and sens2.value == 1:
        #relay_1.value(0)
        print('INFO: Well draining procedure started')
        while time.time() < (time_start + max_pump_time):
            set_reset = True
            sens1.pull_sensor()
            sens2.pull_sensor()
            if sens1.value > sens2.value or sens1.value == sens2.value:
                time_calculated = int(time.time() - time_start)
                print('INFO: Still draining [{}s - {}:{} - {}:{}]'.format(time_calculated, sens1.position, sens1.value, sens2.position, sens2.value))
                time.sleep(1)
            else:
                set_reset = False
                #relay_1.value(1)
                print('WARN: WTF, This should not be possible - {}:{} - {}:{}'.format(sens1.position, sens1.value, sens2.position, sens2.value))
                break # Turn of relay if this is a possibility, to be on the safe side
        set_reset = False
        #time.sleep(1)

    # Not water
    elif sens1.value == 0 and sens2.value == 0:
        #relay_1.value(1)
        print('INFO - No water in the well!')
        #time.sleep(1)

    # Filling up
    elif sens1.value == 1 and sens2.value == 0:
        #relay_1.value(1)
        print('INFO - Well is filling')
        #time.sleep(1)

    # Top sensor is stuck
    elif sens1.value == 0 and sens2.value == 1:
        print('ERROR: Top sensor is probably stuck')

    # Nothing
    else:
        #relay_1.value(1)
        print('Do nothing')
        #time.sleep(1)

while True:
    pump_function()
