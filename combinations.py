from time import sleep_us
import time
from machine import Pin, PWM, time_pulse_us


NOTE_B0 = 31
NOTE_C1 = 33
NOTE_CS1 = 35
NOTE_D1 = 37
NOTE_DS1 = 39
NOTE_E1 = 41
NOTE_F1 = 44
NOTE_FS1 = 46
NOTE_G1 = 49
NOTE_GS1 = 52
NOTE_A1 = 55
NOTE_AS1 = 58
NOTE_B1 = 62
NOTE_C2 = 65
NOTE_CS2 = 69
NOTE_D2 = 73
NOTE_DS2 = 78
NOTE_E2 = 82
NOTE_F2 = 87
NOTE_FS2 = 93
NOTE_G2 = 98
NOTE_GS2 = 104
NOTE_A2 = 110
NOTE_AS2 = 117
NOTE_B2 = 123
NOTE_C3 = 131
NOTE_CS3 = 139
NOTE_D3 = 147
NOTE_DS3 = 156
NOTE_E3 = 165
NOTE_F3 = 175
NOTE_FS3 = 185
NOTE_G3 = 196
NOTE_GS3 = 208
NOTE_A3 = 220
NOTE_AS3 = 233
NOTE_B3 = 247
NOTE_C4 = 262
NOTE_CS4 = 277
NOTE_D4 = 294
NOTE_DS4 = 311
NOTE_E4 = 330
NOTE_F4 = 349
NOTE_FS4 = 370
NOTE_G4 = 392
NOTE_GS4 = 415
NOTE_A4 = 440
NOTE_AS4 = 466
NOTE_B4 = 494
NOTE_C5 = 523
NOTE_CS5 = 554
NOTE_D5 = 587
NOTE_DS5 = 622
NOTE_E5 = 659
NOTE_F5 = 698
NOTE_FS5 = 740
NOTE_G5 = 784
NOTE_GS5 = 831
NOTE_A5 = 880
NOTE_AS5 = 932
NOTE_B5 = 988
NOTE_C6 = 1047
NOTE_CS6 = 1109
NOTE_D6 = 1175
NOTE_DS6 = 1245
NOTE_E6 = 1319
NOTE_F6 = 1397
NOTE_FS6 = 1480
NOTE_G6 = 1568
NOTE_GS6 = 1661
NOTE_A6 = 1760
NOTE_AS6 = 1865
NOTE_B6 = 1976
NOTE_C7 = 2093
NOTE_CS7 = 2217
NOTE_D7 = 2349
NOTE_DS7 = 2489
NOTE_E7 = 2637
NOTE_F7 = 2794
NOTE_FS7 = 2960
NOTE_G7 = 3136
NOTE_GS7 = 3322
NOTE_A7 = 3520
NOTE_AS7 = 3729
NOTE_B7 = 3951
NOTE_C8 = 4186
NOTE_CS8 = 4435
NOTE_D8 = 4699
NOTE_DS8 = 4978

class MeasurementTimeout(Exception):
    def __init__(self, timeout):
        super().__init__("Measurement timeout, exceeded {} us".format(timeout))


class Ultrasonic(object):
    def __init__(self, trigger_pin, echo_pin, timeout_us=30000):

        self.timeout = timeout_us

        # Init trigger pin (out)
        self.trigger = Pin(trigger_pin, mode=Pin.OUT, pull=None)
        self.trigger.off()

        # Init echo pin (in)
        self.echo = Pin(echo_pin, mode=Pin.IN, pull=None)

    def distance_in_inches(self):
        return (self.distance_in_cm() * 0.3937)

    def distance_in_cm(self):
        # Send a 10us pulse
        self.trigger.on()
        sleep_us(10)
        self.trigger.off()

        # Wait for the pulse and calc its duration
        time_pulse = time_pulse_us(self.echo, 1, self.timeout)

        if time_pulse < 0:
            raise MeasurementTimeout(self.timeout)

        # Divide the duration of the pulse by 2 (round-trip) and then divide it
        # by 29 us/cm (speed of sound = ~340 m/s)
        return (time_pulse / 2) / 29
    
    

sensor = Ultrasonic(23, 5)
buzz = PWM(Pin(33))
buzz.duty(0)




while True:
    try:
        dist = sensor.distance_in_cm()
        print("Dist = {}".format(dist))
        
#         Check for distance and tone
        if dist > 2 and dist < 6:
            buzz.freq(NOTE_C6)
            buzz.duty(500)
        elif dist > 8 and dist < 12:
            buzz.freq(NOTE_D6)
            buzz.duty(500)
        elif dist > 14 and dist < 18:
            buzz.freq(NOTE_E6)
            buzz.duty(500)
        elif dist > 20 and dist < 24:
            buzz.freq(NOTE_F6)
            buzz.duty(500)
        elif dist > 26 and dist < 30:
            buzz.freq(NOTE_G6)
            buzz.duty(500)
        elif dist > 32 and dist < 36:
            buzz.freq(NOTE_A6)
            buzz.duty(500)
        elif dist > 38 and dist < 42:
            buzz.freq(NOTE_B6)
            buzz.duty(500)
        elif dist > 44 and dist < 48:
            buzz.freq(NOTE_C7)
            buzz.duty(500)
        else:
            buzz.duty(0)

    except MeasurementTimeout as e:
        print("{}".format(e))
        buzz.duty(0)

