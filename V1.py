try:
    from Notify import Main as NotifyMain
    Notify = NotifyMain()
except(ImportError):
    print("[!] Failed to import Notify.")
    exit()

Notify.SetMode("C")
Notify.Success("Imported Notify (Mode C)")

# Inputs
InputOne = 0
InputTwo = 0
InputThree = 0
InputFour = 0

#outputs

Fuel = 3
OilWarning = 5
BatteryWarning = 7
Handbrake = 8
BrakeLining = 10
BrakeWarning = 12
Backlight = 11
IndicateLeft = 13
IndicateRight = 15
MainBeam = 16
ABS = 18

Notify.Info("Beginning Hardware Setup")

try:
    import RPi.GPIO as GPIO
    Notify.Success("Imported GPIO Modules.")
    GPIOstate = True
except(ImportError):
    Notify.Warning("Failed to import GPIO Modules. Attempting substitute...")
    GPIOstate = False
    try:
        from EmulatorGUI import GPIO
        Notify.Success("Imported eGPIO Modules.")
    except(ImportError):
        print("Failed to import GPIO Modules.")

class Master:
    def __init__(self):
        if GPIOstate:
            self.Setup()
        else:
            self.eSetup()

    def eSetup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.cleanup()
        GPIO.setup(Fuel, GPIO.OUT)
        GPIO.setup(OilWarning, GPIO.OUT)
        GPIO.setup(BatteryWarning, GPIO.OUT)
        GPIO.setup(Handbrake, GPIO.OUT)
        GPIO.setup(BrakeLining, GPIO.OUT)
        GPIO.setup(Backlight, GPIO.OUT)
        GPIO.setup(IndicateLeft, GPIO.OUT)
        GPIO.setup(IndicateRight, GPIO.OUT)
        GPIO.setup(MainBeam, GPIO.OUT)
        GPIO.setup(ABS, GPIO.OUT)

    def Setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.cleanup()
        GPIO.setup(Fuel, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(OilWarning, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(BatteryWarning, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(Handbrake, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(BrakeLining, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(Backlight, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(IndicateLeft, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(IndicateRight, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(MainBeam, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(ABS, GPIO.OUT, initial=GPIO.HIGH)


class Indicator:
    def __init__(self):
        pass

    def CheckLamps(self):
        GPIO.output()

Controller = Master()



