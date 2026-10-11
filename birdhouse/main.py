## Main Script ##

## Definitions ##
from ipaddress import IPv4Address
from datetime import datetime as dt, timedelta as td
import board
class Settings:
    class PinMap:
        DHT: board.pin = board.D17 # type: ignore
        PIR: board.pin = board.D18 # type: ignore
        # Control Pins:
        EmergencyPowerFlag: board.pin = board.D19 # type: ignore
        PowerIndicatorFlag: board.pin = board.D20 # type: ignore
        TriggerIndicatorFlag: board.pin = board.D21 # type: ignore

    ServerEndpoint: str | None = None
    IP: IPv4Address = IPv4Address("10.0.0.217")
    WiFiCredentials: tuple[str, str] = ("Conallin's WiFi", "67205776")
    LuminosityCutoff: int = 30
    AlarmDelay: td = td(minutes=30)


## BEGIN ##
if __name__ == "__main__":
    # Start RTC & save current timestamp
    import adafruit_ds3231
    RTC = adafruit_ds3231.DS3231(board.I2C())
    START_TIMESTAMP = dt(year=RTC.datetime.tm_year, month=RTC.datetime.tm_mon, day=RTC.datetime.tm_mday, hour=RTC.datetime.tm_hour, minute=RTC.datetime.tm_min)

    ## Check flags
    from classes import Flags
    FLAGS = Flags()

    # If currently running on Emergency Power:
    if (FLAGS.EmergencyPower):
        # NETWORK CONNECT wifi (or other communication method)
        # TODO
        # new payload -> emergency power warning
        # NETWORK SEND payload => Home Server
        from classes import EmergencyPayload
        EmergencyPayload().push()
        # NETWORK DISCONNECT wifi
        # TODO
        # communicates to power controller to cut power.
        exit()
    # ENDIF

    ## Begin normal operation
    # new payload -> empty
    from classes import Payload
    payload = Payload()

    # INPUT data = sensor array input
    import adafruit_bh1750, adafruit_dht
    LightSensor = adafruit_bh1750.BH1750(board.I2C())
    DHT22 = adafruit_dht.DHT22(Settings.PinMap.DHT)

    # payload <- data
    payload.load([
        ("lux", LightSensor.lux),
        ("temperature", DHT22.temperature),
        ("humidity", DHT22.humidity),
        ("battery", FLAGS.PowerIndicatorFlag),
        ("trigger", FLAGS.TriggerIndicatorFlag)
    ])
    
    # IF (data.luminosity > luminosity cutoff)
    if (LightSensor.lux > Settings.LuminosityCutoff):
        # sun is up
        # INPUT recording = 15s video recording from camera and mic
        # payload <- recording
        from recording import record
        payload.video(record())
    # ENDIF

    # NETWORK CONNECT wifi
    # NETWORK SEND payload => Home Server
    payload.push()

    ## Updates
    # TODO
    # INPUT updates = NETWORK GET Updates <= Home Server

    # IF (updates is not empty)
        # FOR command in updates
            # EXECUTE command
            # NETWORK SEND result => Home Server
        # ENDFOR
    # ENDIF


    ## Re-arm RTC if needed
    # IF (trigger == clock)
    if (FLAGS.TriggerIndicatorFlag == Flags.States.ALARM):
        # I2C SEND start_time + Alarm delay => rtc alarm
        RTC.alarm1_status = False
        RTC.alarm1_interrupt = True
        RTC.alarm1 = ((START_TIMESTAMP + Settings.AlarmDelay).timetuple(), "daily")
    # ENDIF

    # I2C DISCONNECT rtc (no need)
    # NETWORK DISCONNECT wifi
    # QUIT # communicates to power controller to cut power.
    #END
    exit()