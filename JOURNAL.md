# Development Journal
> This is a development journal containing recaps on the work I've done towards this project.

## Tuesday, 22nd September 2026
Today is my first planning day. I've done some cursory planning in a notebook, which I will describe here.
The basic idea for this project is to record the birds visiting the birdhouse for food, and send it back to a home server along with some environmental readings. The system will be housed inside of one of those wooden birdhouses you can find at Bunnings, and will have a birdseed tray attached to the front. I've brainstormed the following requirements:
- [ ] Must be self-sufficient, enough to run to more than a day without physical wiring such as networking or power. This allow for more placement options.
- [ ] Must have equipment capable of recording video and audio, and for collecting environmental data such as temperature, humidity and luminosity
- [ ] Must be able to take video recordings after being triggered by either the PIR sensor or at 30 minute intervals while the sun is up. When the sun is down, take only sensor captures.
- [ ] Must be able to access recording data and videos at any time from an accessible interface.
With these requirements, I've come up with a rough idea. The project will consist of three main parts: The Battery section, the Pi section, and the Server section.
### The Battery Section
In order to sustain itself without access to any mains power, the birdhouse needs it's own way to source and store power. This will come in the form of 4 rechargeable AA batteries, some solar panels and a charging circuit to prevent overcharge. In addition to this, a micro-controller, most likely an Arduino UNO for the prototype, will be used to control the power supply to the Pi. Unsurprisingly, running a full Linux distro is going to chew through a couple AAs pretty fast, so in order to minimise power draw, the Pi will have it's power disconnected by the UNO when in downtime.
![[battery_section_flowchart.png]]
### The Pi Section
The Pi will be connected to an array of a camera, a microphone, and as of now, the following sensors:
- DHT22 for Temperature and Humidity readings
- Luminosity sensor
I may add more later. The Pi will run a diskless Alpine OS, to allow it to boot extremely fast and cut power without damaging the disk. When ever the Pi boots up, it will check the control pins for information on battery status, and the trigger before launching it's main script. This will either be in Python or C, I haven't decided. The following is an approximation of the pseudo-code:
```
# ON BOOT:
BEGIN
	I2C CONNECT rtc
	INPUT start_time = rtc time
	
	# Check flags
	IF (emergency_power_flag == true)
		NETWORK CONNECT wifi (or other communication method)
		new payload -> emergency power warning
		NETWORK SEND payload => Home Server
		NETWORK DISCONNECT wifi
		QUIT # communicates to power controller to cut power.
	ENDIF
	
	# Begin normal operation
	new payload -> empty
	INPUT data = sensor array input
	payload <- data
	
	INPUT battery = power controller battery flags
	payload <- battery
	
	IF (data.luminosity > luminosity cutoff)
		# sun is up
		INPUT recording = 15s video recording from camera and mic
		payload <- recording
	ENDIF
	
	NETWORK CONNECT wifi
	NETWORK SEND payload => Home Server
	
	# Updates
	INPUT updates = NETWORK GET Updates <= Home Server
	
	IF (updates is not empty)
		FOR command in updates
			EXECUTE command
			NETWORK SEND result => Home Server
		ENDFOR
	ENDIF
	
	# Re-arm RTC if nesscercary
	IF (trigger == clock)
		I2C SEND start_time + 30mins => rtc alarm
	ENDIF
	
	I2C DISCONNECT rtc
	NETWORK DISCONNECT wifi
	QUIT # communicates to power controller to cut power.
END
```
> Note: finish later
## Wednesday, 23 September 2026
Today I started having a look at the viability of Python for the Pi section of the project. The Pi needs to be able to do a couple of things:
- Read I2C for the RTC
- Read GPIO for the sensor data & control flags.
- Record audio + video and store **IN MEMORY** due to the Pi being diskless
- Manipulate WiFi and send data to an external server.
