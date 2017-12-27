# Control a heat lamp in a Proofing Drawer
# BW ST

import Adafruit_DHT
from time import sleep
import RPi.GPIO as GPIO #imports the input output pin libries

class PDGlobals():
    temperature = 9001
    humidity = 00
    desiredTemp = 85
    proofLoopOff = True


class ProofingDrawer(object):
    GPIO.cleanup()
    relayPin = 17
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(relayPin, GPIO.OUT) #tells GPIO that our relay pin will be a 5v (output pin)
    
                    
    def __init__(self):
        if(PDGlobals.proofLoopOff == True):
            self.turn_off_light()
        else:
            self.check_temp()

    def get_temperature_humidity(self):
        # Try to grab a sensor reading.  Use the read_retry method which will retry up
        # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
        humidity, temperature = (Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 4, delay_seconds=3))
        
        #makes temperature read in Farenheit
        PDGlobals.temperature = temperature * 9/5.0 + 32
        PDGlobals.humidity = humidity
        return([humidity, PDGlobals.temperature])
    
    def turn_on_light(self):
        #turn on light at x degrees farenheit
        GPIO.output(self.relayPin, GPIO.HIGH) #sets state of pin LOW = off, High = on
        

    def turn_off_light(self):
        #turn off light at x degrees farenheit
        GPIO.output(self.relayPin, GPIO.LOW) #sets state of pin LOW = off, High = on


    #make a call to turn off light function and turn on light function 
    def check_temp(self):
       
        while not PDGlobals.proofLoopOff:
            #change so it only reads from temperature, not humidity
            try:
                temperature = self.get_temperature_humidity()[1]
            except:
                print("Temp not read, reaturned: {}f".format(temperature))
                temperature = PDGlobals.temperature
            if temperature < PDGlobals.desiredTemp - 1 and PDGlobals.proofLoopOff == False:
                self.turn_on_light()
                print("light ON with: {}f".format(temperature))

            elif temperature > PDGlobals.desiredTemp + 1:
                self.turn_off_light()
                print("light OFF with: {}f".format(temperature))
                
            sleep(2)
        
        self.turn_off_light()