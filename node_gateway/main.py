#! /bin/python3

import time

## TODO: Get some feedback system to determine if pump is running

class PumpObject:
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.powered_on = False
        self.temprature = Null
        self.pump_start_time = Null
        self.pump_stop_time = Null

    def get_status(self):
        if self.powered_on == True:
            temporary_stop_time = time.time()
            print("INFO: Pump is running [Time running: {}]".format((temporary_stop_time - self.pump_start_time)))
            return True
        else:
            return False

    def get_time_since_start(self):
        temporary_stop_time = time.time()
        print("INFO: Time since start: {}]".format((temporary_stop_time - self.pump_start_time)))
        return (temporary_stop_time - self.pump_start_time)

    def start_pump(self):
        if self.powered_on == False:
            print("INFO: Attempting to start the pump")
            ## TODO: Run try function to initiate GPIO pin to start pump. Possible feedback?
            self.powered_on = True
            self.pump_start_time = time.time()
        else:
            temporary_stop_time = time.time()
            print("INFO: Pump is already running [Time running: {}]".format((temporary_stop_time - self.pump_start_time)))

    def stop_pump(self):
        if self.powered_on == True:
            print("INFO: Attempting to stop the pump")
            ## TODO: Run try function to initiate GPIO pin to stop pump. Possible feedback?
            self.powered_on = False
            self.pump_stop_time = time.time()
            print("INFO: Time running: {}".format((self.pump_stop_time - self.pump_start_time)))
        else:
            print("INFO: Pump already stopped")
            print("INFO: Time running: {}".format((self.pump_stop_time - self.pump_start_time)))