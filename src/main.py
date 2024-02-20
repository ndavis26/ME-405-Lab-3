"""! @file main.py
Defines Servo class.
If this is the main.py file on the Nucleo,
it will run a motor response test.
@author Nathaniel Davis
@author Sebastian Bessoudo
@date 02-13-2024
"""

import micropython
import pyb
import time
import cqueue
from motor_driver_updated import MotorDriver
from encoder_reader_updated import Encoder

# Allow interrupts to display errors
micropython.alloc_emergency_exception_buf(100)

class Servo:  
    def __init__(self, motor, encoder):
        self.motor = motor
        self.encoder = encoder
        self.Kp = 0.1
        self.error = 0
        
    def run(self, level):
        self.motor.set_duty_cycle(level)
        
    def set_setpoint(self, setpoint):
        self.encoder.read()
        self.error = setpoint - self.encoder.pos
        self.PWM = self.Kp*self.error
        self.motor.set_duty_cycle(self.PWM)
        
    def set_Kp(self, Kp):
        self.Kp = Kp
        
    
if __name__ == "__main__":  
    # run motor response test
    moe = MotorDriver(pyb.Pin.board.PA10, pyb.Pin.board.PB4, 1,  pyb.Pin.board.PB5, 2, 3)
    enc = Encoder(pyb.Pin.board.PC6, pyb.Pin.board.PC7, 8, 1, 2)
    serv = Servo(moe, enc)
    num = 500
    while True:
        input_kp = float(input('Please input a value for Kp: '))
        serv.set_Kp(input_kp)
        input_setp = int(input('Please input a value for the setpoint: '))
        serv.set_setpoint(input_setp)
        
        positions = []
        times = [10*x for x in range(num)]
        for n in range(num):
            serv.set_setpoint(input_setp)
            time.sleep_ms(10)
            positions.append(serv.encoder.read())
            print(f"{times[n]}, {serv.encoder.read()}")
        serv.run(0)
        print('End')
            
    