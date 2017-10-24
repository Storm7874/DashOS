class Lamp():
    def __init__(self, PinNumber):
        self.Pin = PinNumber
        self.State = False

    def Enable(self):
        if self.State == True:
            GPIO.output(self.Pin, GPIO.HIGH)
        else:
            pass

    def Disable(self):
        if self.State == False:
            GPIO.output(self.Pin, GPIO.LOW)
        else:
            pass

    def Status(self):
        if self.State == True:
            return True
        else:
            return False


Oil = Lamp(OilPin)
Handbrake = Lamp