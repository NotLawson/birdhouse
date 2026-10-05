import board, digitalio
from adafruit_ds3231 import DS3231
from adafruit_bh1750 import BH1750
from adafruit_dht import DHT22
from time import sleep

### Settings & Definitions
class Settings:
    class PinMap:
        DHT: board.pin = board.D17 # type: ignore
        PIR: board.pin = board.D18 # type: ignore

# Initialise devices
class Devices:
    DHT = DHT22(Settings.PinMap.DHT)
    PIR = digitalio.DigitalInOut(Settings.PinMap.PIR)
    i2C = board.I2C()
    RTC = DS3231(i2C)
    LightIntensity = BH1750(i2C)

Devices.PIR.direction = digitalio.Direction.INPUT

# Grab readings
while True:
    try:      
        print(f"DHT TEMP: {round(Devices.DHT.temperature or 0, 2)} DHT HUMIDITY: {round(Devices.DHT.humidity or 0, 2)} BH1750 LUX: {round(Devices.LightIntensity.lux or 0, 2)} DS3231 TIME: {str(Devices.RTC.datetime)} DS3231 TEMP: {round(Devices.RTC.temperature or 0, 2)}", end = "\r")
        sleep(0.5)
    except RuntimeError:
        pass
    except KeyboardInterrupt:
        exit()
