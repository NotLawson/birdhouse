
class Flags:
    def __init__(self):
        import digitalio
        from main import Settings
        self._emergencyPowerFlag: digitalio.DigitalInOut = digitalio.DigitalInOut(Settings.PinMap.EmergencyPowerFlag)
        self._powerIndicatorFlag: digitalio.DigitalInOut = digitalio.DigitalInOut(Settings.PinMap.PowerIndicatorFlag)
        self._triggerIndicatorFlag: digitalio.DigitalInOut = digitalio.DigitalInOut(Settings.PinMap.TriggerIndicatorFlag)

        self._emergencyPowerFlag.direction = digitalio.Direction.INPUT
        self._powerIndicatorFlag.direction = digitalio.Direction.INPUT
        self._triggerIndicatorFlag.direction = digitalio.Direction.INPUT

    class States:
            FULL = "FULL"
            STANDARD = "STANDARD"
            ALARM = "ALARM"
            MOTION = "MOTION"

    @property
    def EmergencyPower(self):
        return self._emergencyPowerFlag.value

    @property
    def PowerIndicatorFlag(self):
        return self.States.FULL if self._powerIndicatorFlag.value else self.States.STANDARD

    @property
    def TriggerIndicatorFlag(self):
        return self.States.ALARM if self._powerIndicatorFlag.value else self.States.MOTION
    
class Payload:
    def __init__(self):
        from main import Settings
        from requests import Request, Session, Response
        self._session: Session = Session()
        self._request: Request = Request(method="POST", url=Settings.ServerEndpoint or "placeholder")
        self._response: Response | None = None

        self._body: list[tuple] = []
        self._mock: bool = False if (Settings.ServerEndpoint) else True


    def load(self, content: list[tuple]) -> None:
        self._body += content
        return
    
    from io import BytesIO
    def video(self, file: BytesIO) -> None:
        self._files = {"video": file}
        return

    def push(self):
        # submit payload to server
        if self._mock:
            from requests import Response
            from json import dump, dumps

            from __main__ import START_TIMESTAMP
            dump(self._body, open(f"mocks/{START_TIMESTAMP.strftime('%d-%m-%Y %H:%M:%S'),}/data.json", "w"))
            if "video" in self._files.keys():
                open(f"mocks/{START_TIMESTAMP.strftime('%d-%m-%Y-%H:%M:%S')}/clip.mp4", "wb").write(self._files["video"].getbuffer())
            
            self._response = Response()
            self._response.status_code = 200
            self._response._content = dumps({"message":"Successfully Submitted Payload"}).encode("utf-8")
            return self._response
        self._request.data = self._body
        self._request.files = self._files
        return self._session.send(self._request.prepare())

    @property
    def status(self) -> int | None:
        return None if (self._response == None) else self._response.status_code


class EmergencyPayload(Payload):
    def __init__(self):
        super().__init__()
        self.load([("EmergencyPower", True)])


class Network:
    def __init__(self):
        from main import Settings
        self._credentials = Settings.WiFiCredentials