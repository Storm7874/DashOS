FirstRun = True
import random
import os
import datetime
try:
    from Notify import Main as NotifyMain
    Notify = NotifyMain()
except(ImportError):
    print("Failed to import Notify")
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

try:
    from utilsv2 import Main as UtilsMain
except(ImportError):
    print("Failed to import Utils")
utils = UtilsMain()
import time

OilPin = 3
HandbrakePin = 5
LeftIndicatorPin = 7
RightIndicatorPin = 8
BacklightPin = 10
ParkBrakePin = 12
BrakeWarningPin = 11
MainPowerPin = 13
HighTempPin = 15
LowFuelPin = 16
BatteryPin = 18


class Lamp:
    def __init__(self, PinNumber):
        self.pin = PinNumber
        self.Status = False

    def Enable(self):
        GPIO.output(self.pin, GPIO.HIGH)
        self.Status = True

    def Disable(self):
        GPIO.output(self.pin, GPIO.LOW)
        self.Status = False

    def Flash(self, count, freq):
        for x in range(0, count):
            self.Enable()
            time.sleep(freq)
            self.Disable()

    def Status(self):
        return self.Status


class Power:
    def __init__(self):
        self.Pin = MainPowerPin
        self.Status = False

    def PowerOn(self):
        GPIO.output(self.Pin, GPIO.HIGH)
        Notify.Success("Power On")
        self.Status = True

    def PowerOff(self):
        GPIO.output(self.Pin, GPIO.LOW)
        Notify.Success("Power Off")
        self.Status = False

    def MainPowerStatus(self):
        if self.Status == True:
            return True
        elif self.Status == False:
            return False


class Indicator:
    def __init__(self):
        self.PinNumbers = [3,5,7,8,10,12,11,13,15,16,18]

    def eSetup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        Notify.Success("Completed GPIO Setup")
        GPIO.setup(3, GPIO.OUT)
        GPIO.setup(5, GPIO.OUT)
        GPIO.setup(7, GPIO.OUT)
        GPIO.setup(8, GPIO.OUT)
        GPIO.setup(10, GPIO.OUT)
        GPIO.setup(12, GPIO.OUT)
        GPIO.setup(11, GPIO.OUT)
        GPIO.setup(13, GPIO.OUT)
        GPIO.setup(15, GPIO.OUT)
        GPIO.setup(16, GPIO.OUT)
        GPIO.setup(18, GPIO.OUT)
        Notify.Success("Outputs setup")

    def Setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        Notify.Success("Completed GPIO Setup")
        for count in range(0, len(self.PinNumbers)):
            GPIO.setup(self.PinNumbers[count], initial=GPIO.LOW)
        Notify.Success("Outputs Setup")

    def PreInit(self):
        if GPIOstate == True:
            self.Setup()
        else:
            self.eSetup()


Oil = Lamp(OilPin)
Handbrake = Lamp(HandbrakePin)
LeftIndicator = Lamp(LeftIndicatorPin)
RightIndicator = Lamp(RightIndicatorPin)
Backlight = Lamp(BacklightPin)
ParkBrake = Lamp(ParkBrakePin)
BrakeWarning = Lamp(BrakeWarningPin)
## Main Power is seperate
HighTemp = Lamp(HighTempPin)
LowFuel = Lamp(LowFuelPin)
Battery = Lamp(BatteryPin)
Controller = Indicator()
Controller.PreInit()
PowerControl = Power()

class Procedures():
    def __init__(self):
        self.IndicatorFreq = 0.5

    def AllOff(self):
        Oil.Disable()
        Handbrake.Disable()
        LeftIndicator.Disable()
        RightIndicator.Disable()
        Backlight.Disable()
        ParkBrake.Disable()
        BrakeWarning.Disable()
        HighTemp.Disable()
        LowFuel.Disable()
        Battery.Disable()
        Notify.Info("All Off")

    def AllOn(self):
        Oil.Enable()
        Handbrake.Enable()
        LeftIndicator.Enable()
        RightIndicator.Enable()
        Backlight.Enable()
        ParkBrake.Enable()
        BrakeWarning.Enable()
        HighTemp.Enable()
        LowFuel.Enable()
        Battery.Enable()
        Notify.Info("All On")

    def BacklightOnly(self):
        self.AllOff()
        Backlight.Enable()

    def Acc(self):
        self.AllOff()
        Oil.Enable()
        Handbrake.Enable()
        Battery.Enable()

    def RandomSelection(self):
        Lamps = ["Oil","Handbrake","LI","RI","Backlight","ParkBrake",
                 "BrakeWarning","HighTemp","LowFuel","Battery"]
        SelectedIDs = []
        for count in range(0,(random.randint(2,5))):
            SelectedIDs.append(random.choice(Lamps))
        Notify.Info("{} Lamps selected.".format(len(SelectedIDs)))
        for count in range(0,len(SelectedIDs)):
            if SelectedIDs[count] == "Oil":
                Oil.Enable()
            elif SelectedIDs[count] == "Handbrake":
                Handbrake.Enable()
            elif SelectedIDs[count] == "LI":
                LeftIndicator.Enable()
            elif SelectedIDs[count] == "RI":
                RightIndicator.Enable()
            elif SelectedIDs[count] == "Backlight":
                Backlight.Enable()
            elif SelectedIDs[count] == "ParkBrake":
                ParkBrake.Enable()
            elif SelectedIDs[count] == "BrakeWarning":
                BrakeWarning.Enable()
            elif SelectedIDs[count] == "HighTemp":
                HighTemp.Enable()
            elif SelectedIDs[count] == "LowFuel":
                LowFuel.Enable()
            elif SelectedIDs[count] == "Battery":
                Battery.Enable()

    def PowerOff(self):
        PowerControl.PowerOff()

    def PowerOn(self):
        PowerControl.PowerOn()

    def BrakesOnly(self):
        Handbrake.Enable()
        ParkBrake.Enable()
        BrakeWarning.Enable()

    def Warnings(self):
        Oil.Enable()
        Handbrake.Enable()
        BrakeWarning.Enable()
        HighTemp.Enable()
        LowFuel.Enable()
        Battery.Enable()

Proc = Procedures()



class Interface:
    def __init__(self):
        self.Hour = ""
        self.Minute = ""

    def Proc(self):
        os.system("clear")
        print("""
        |------------------------------------------------------------------|
        |                           Procedures                             |
        |------------------------------------------------------------------|
        |   [1] Left Indicator                                             |
        |   [2] Right Indicator                                            |
        |   [3] All On                                                     |
        |   [4] All Off                                                    |
        |   [5] Backlight Only                                             |
        |   [6] Brakes                                                     |
        |   [7] Warnings                                                   |
        |   [8] Low Fuel                                                   |
        |   [9] Random                                                     |
        |   [10] Status Mode                                               |
        |------------------------------------------------------------------|
        |   [11] Back                                           {}:{}      |
        |------------------------------------------------------------------|
        """.format(self.Hour, self.Minute))
        while True:
            try:
                Notify.Green()
                menuchoice = int(input(">"))
                Notify.ClearColour()
                if menuchoice not in [1,2,3,4,5,6,7,8,9,10,11]:
                    Notify.Error("Please enter a valid number.")
                else:
                    break
            except(ValueError):
                Notify.Error("Please enter a valid number")
        if menuchoice == 1:
            while True:
                try:
                    LeftIndicator.Flash(500, 1)
                except(KeyboardInterrupt):
                    LeftIndicator.Disable()
        elif menuchoice == 2:
            while True:
                try:
                    RightIndicator.Flash(500, 1)
                except(KeyboardInterrupt):
                    RightIndicator.Disable()
        elif menuchoice == 3:
            Proc.AllOn()
        elif menuchoice == 4:
            Proc.AllOff()
        elif menuchoice == 5:
            Proc.BacklightOnly()
        elif menuchoice == 6:
            Proc.BrakesOnly()
        elif menuchoice == 7:
            Proc.Warnings()
        elif menuchoice == 8:
            LowFuel.Enable()
        elif menuchoice == 9:
            Proc.RandomSelection()
        elif menuchoice == 10:
            Status.StatusModeLoop()
        elif menuchoice == 11:
            os.system("clear")
            self.Main()
        self.Proc()

    def ManControl(self):
        os.system("clear")
        Haz = False
        print("""
        |-----------------------------------------------------------------------------|
        |                               Manual Control                                |
        |-----------------------------------------------------------------------------|
        |   |--------------------|  |--------------------|  |--------------------|    |
        |       Red Indicators            Indicators                 Other            |
        |       [1] Oil                 [7] Left                [10] Backlight        |
        |       [2] Handbrake           [8] Right               [11] Low Fuel         |
        |       [3] Hi Temp             [9] Hazards                                   |
        |       [4] Park Brake                                                        |
        |       [5] Battery                                                           |
        |       [6] Brake Warn                                                        |
        |                                                                             |
        |-----------------------------------------------------------------------------|
        |   [99] Flash Mode     [100] Back      [102] Exit                   {}:{}    |
        |-----------------------------------------------------------------------------|

        """.format(self.Hour, self.Minute))
        while True:
            try:
                lampchoice = int(input("> "))
                if lampchoice not in [1,2,3,4,5,6,7,8,9,10,11,99,100,102]:
                    Notify.Error("Please enter a valid number")
                else:
                    break
            except(ValueError):
                Notify.Error("Please enter a valid number")
        if lampchoice == 1:
            if Oil.Status:
                Oil.Disable()
            elif not Oil.Status:
                Oil.Enable()
        elif lampchoice == 2:
            if Handbrake.Status:
                Handbrake.Disable()
            elif not Handbrake.Status:
                Handbrake.Enable()
        elif lampchoice == 3:
            if HighTemp.Status:
                HighTemp.Disable()
            elif not HighTemp.Status:
                HighTemp.Enable()
        elif lampchoice == 4:
            if ParkBrake.Status:
                ParkBrake.Disable()
            elif not ParkBrake.Status:
                ParkBrake.Enable()
        elif lampchoice == 5:
            if Battery.Status:
                Battery.Disable()
            elif not Battery.Status:
                Battery.Enable()
        elif lampchoice == 6:
            if BrakeWarning.Status:
                BrakeWarning.Disable()
            elif not BrakeWarning.Status:
                BrakeWarning.Enable()
        elif lampchoice == 7:
            if LeftIndicator.Status:
                LeftIndicator.Disable()
            elif not LeftIndicator.Status:
                LeftIndicator.Enable()
        elif lampchoice == 8:
            if RightIndicator.Status:
                RightIndicator.Disable()
            elif not RightIndicator.Status:
                RightIndicator.Enable()
        elif lampchoice == 9:
            if Haz == False:
                if RightIndicator.Status == True or LeftIndicator.Status == True:
                    LeftIndicator.Disable()
                    RightIndicator.Disable()
                LeftIndicator.Enable()
                RightIndicator.Enable()
            elif Haz == True:
                if RightIndicator.Status == False or LeftIndicator.Status == False:
                    LeftIndicator.Enable()
                    RightIndicator.Enable()
                LeftIndicator.Disable()
                RightIndicator.Disable()
        elif lampchoice == 10:
            if Backlight.Status:
                Backlight.Disable()
            elif not Backlight.Status:
                Backlight.Enable()
        elif lampchoice == 11:
            if LowFuel.Status:
                LowFuel.Disable()
            elif not LowFuel.Status:
                LowFuel.Enable()
        elif lampchoice == 99:
            Notify.Info("Please enter the indicator you wish to flash")
            Notify.Cyan()
            FlashNo = 0
            Frequency = 0
            Count = 0
            while True:
                try:
                    FlashNo = int(input("> "))
                    if FlashNo not in [1,2,3,4,5,6,7,8,9,10,11]:
                        Notify.Error("Please enter a correct number")
                    else:
                        break
                except(ValueError):
                    Notify.Error("Please enter a correct number")
            while True:
                try:
                    Frequency = int(input("FREQ> "))
                    break
                except(ValueError):
                    Notify.Error("Please enter a correct number")
            while True:
                try:
                    Count = int(input("COUNT> "))
                    break
                except(ValueError):
                    Notify.Error("Please enter a correct number")
            Notify.ClearColour()
            if FlashNo == 1:
                Oil.Flash(Count, Frequency)
            elif FlashNo == 2:
                Handbrake.Flash(Count, Frequency)
            elif FlashNo == 3:
                HighTemp.Flash(Count, Frequency)
            elif FlashNo == 4:
                ParkBrake.Flash(Count, Frequency)
            elif FlashNo == 5:
                Battery.Flash(Count, Frequency)
            elif FlashNo == 6:
                BrakeWarning.Flash(Count, Frequency)
            elif FlashNo == 7:
                LeftIndicator.Flash(Count, Frequency)
            elif FlashNo == 8:
                RightIndicator.Flash(Count, Frequency)
            elif FlashNo == 9:
                Notify.Warning("Hazards not supported.")
            elif FlashNo == 10:
                Backlight.Flash(Count, Frequency)
            elif FlashNo == 11:
                LowFuel.Flash(Count, Frequency)
        elif lampchoice  == 100:
            self.Main()
        elif lampchoice == 102:
            exit()
        self.ManControl()

    def UpdateTime(self):
        self.Hour = datetime.datetime.today().hour
        self.Minute = datetime.datetime.today().minute

    def Main(self):
        os.system("clear")
        self.UpdateTime()
        print("""
        |------------------------------------------------------------------|
        |                       Dashboard Control Menu                     |
        |------------------------------------------------------------------|
        |   {}:{}     /                                                    |
        |------------/                                                     |
        |                                                                  |
        |   [1] Manual Control                                             |
        |   [2] Procedures                                                 |
        |   [3] Power On                                                   |
        |   [4] Power Off                                                  |
        |   [5] Auto                                                       |
        |                                                                  |
        |------------------------------------------------------------------|
        """.format(self.Hour, self.Minute))
        while True:
            try:
                Notify.Green()
                menuchoice = int(input("> "))
                Notify.ClearColour()
                if menuchoice not in [1,2,3,4,5]:
                    Notify.Error("Please enter a valid number")
                else:
                    break
            except(ValueError):
                Notify.Error("Please enter a valid number")

        if menuchoice == 1:
            self.ManControl()
        elif menuchoice == 2:
            self.Proc()
        elif menuchoice == 3:
            PowerControl.PowerOn()
            self.Main()
        elif menuchoice == 4:
            PowerControl.PowerOff()
            self.Main()
        elif menuchoice == 5:
            Auto.AutoMenu()
UI = Interface()

class StatusMode():
    def __init__(self):
        self.Inputs = [["Flood",False],["Mon",False],
                       ["FanA",False],
                       ["Tape",False],["APSU",False],
                       ["MP",False]]
        self.Flood = 19
        self.Mon = 21
        self.FanA = 22
        self.Tape = 24
        self.APSU = 26
        self.MP = 23
        self.Setup = False

    def SetupInputs(self):
        try:
            GPIO.setup(self.Flood, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.setup(self.Mon, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.setup(self.FanA, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.setup(self.Tape, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.setup(self.APSU, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.setup(self.MP, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            Notify.SetMode("Inputs setup.")
            self.Setup = True
        except():
            Notify.Error("Input setup failed.")

    def CheckForInputs(self):

        if GPIO.input(self.Flood):
            self.Inputs[0][1] = True
        elif GPIO.input(self.Flood) == False:
            self.Inputs[0][1] = False

        if GPIO.input(self.Mon):
            self.Inputs[1][1] = True
        elif GPIO.input(self.Mon) == False:
            self.Inputs[1][1] = False

        if GPIO.input(self.FanA):
            self.Inputs[2][1] = True
        elif GPIO.input(self.FanA) == False:
            self.Inputs[2][1] = False

        if GPIO.input(self.Tape):
            self.Inputs[3][1] = True
        elif GPIO.input(self.Tape) == False:
            self.Inputs[3][1] = False

        if GPIO.input(self.APSU):
            self.Inputs[4][1] = True
        elif GPIO.input(self.APSU) == False:
            self.Inputs[4][1] = False

        if GPIO.input(self.MP):
            self.Inputs[5][1] = True
        elif GPIO.input(self.MP) == False:
            self.Inputs[5][1] = False

    def ActOnInputs(self):
        for count in range(0, len(self.Inputs)):
            if self.Inputs[count][0] == "Flood":
                if self.Inputs[count][1] == True:
                    LeftIndicator.Enable()
                    Notify.Info("Left Indicator Enabled.")
                else:
                    LeftIndicator.Disable()
            elif self.Inputs[count][0] == "Mon":
                if self.Inputs[count][1] == True:
                    RightIndicator.Enable()
                else:
                    RightIndicator.Disable()
            elif self.Inputs[count][0] == "FanA":
                if self.Inputs[count][1] == True:
                    HighTemp.Enable()
                else:
                    HighTemp.Disable()
            elif self.Inputs[count][0] == "Tape":
                if self.Inputs[count][1] == True:
                    ParkBrake.Enable()
                else:
                    ParkBrake.Disable()
            elif self.Inputs[count][0] == "APSU":
                if self.Inputs[count][1] == True:
                    Handbrake.Enable()
                else:
                    Handbrake.Disable()
            elif self.Inputs[count][0] == "MP":
                if self.Inputs[count][1] == True:
                    Battery.Enable()
                else:
                    Battery.Disable()

    def StatusModeDisplay(self):
        os.system("clear")
        os.system("cls")
        AStat = "XXX"
        BStat = "XXX"
        CStat = "XXX"
        DStat = "XXX"
        EStat = "XXX"
        FStat = "XXX"

        for count in range(0,len(self.Inputs)):
            if self.Inputs[count][0] == "Flood":
                if self.Inputs[count][1] == True:
                    EStat = "---"
                elif self.Inputs[count][1] == False:
                    EStat = "XXX"
            if self.Inputs[count][0] == "Mon":
                if self.Inputs[count][1] == True:
                    FStat = "---"
                elif self.Inputs[count][1] == False:
                    FStat = "XXX"
            if self.Inputs[count][0] == "FanA":
                if self.Inputs[count][1] == True:
                    CStat = "---"
                elif self.Inputs[count][1] == False:
                    CStat = "XXX"
            if self.Inputs[count][0] == "Tape":
                if self.Inputs[count][1] == True:
                    BStat = "---"
                elif self.Inputs[count][1] == False:
                    BStat = "XXX"
            if self.Inputs[count][0] == "APSU":
                if self.Inputs[count][1] == True:
                    AStat = "---"
                elif self.Inputs[count][1] == False:
                    AStat = "XXX"
            if self.Inputs[count][0] == "MP":
                if self.Inputs[count][1] == True:
                    DStat  = "---"
                elif self.Inputs[count][1] == False:
                    DStat = "XXX"

        print("""
        |------------------------------------------------------------------|
        |                             Overview                             |
        |------------------------------------------------------------------|
        |   |---INPUTS---|                                |---OUTPUTS---|  |
        |        [A] >>>> --------------[{}]------------- >>> [HBK]       |
        |        [B] >>>> --------------[{}]------------- >>> [PBK]       |
        |        [C] >>>> --------------[{}]------------- >>> [HTP]       |
        |                                                                  |
        |        [D] >>>> --------------[{}]------------- >>> [BAT]       |
        |        [E] >>>> --------------[{}]------------- >>> [LIN]       |
        |        [F] >>>> --------------[{}]------------- >>> [RIN]       |
        |   |------------|                                |-------------|  |
        |------------------------------------------------------------------|
        """.format(AStat,BStat,CStat,DStat,EStat,FStat))

    def StatusModeLoop(self):
        Notify.Info("Status mode Engaged.")
        while True:
            try:
                #Notify.Info("Status mode engaged")
                if self.Setup == False:
                    self.SetupInputs()
                self.CheckForInputs()
                self.ActOnInputs()
                self.StatusModeDisplay()
                time.sleep(1)
            except(KeyboardInterrupt):
                Notify.Warning("Exiting.")
                UI.Main()

class Timer:
    def __init__(self, StartHour, EndHour, Name, Pin):
        self.StartHour = StartHour
        self.EndHour = EndHour
        self.Name = Name
        self.Active = False
        self.CurrentHour = 0
        self.Pin = Pin


    def GetNewTime(self):
        self.CurrentHour = datetime.datetime.today().hour
        self.CurrentHour = int(self.CurrentHour)

    def CheckIfTimerActive(self):
        if self.CurrentHour >= self.StartHour:
            if self.CurrentHour < self.EndHour:
                self.Active = True
        else:
            self.Active = False

    def IsTimerActive(self):
        if self.Active == True:
            return True
        else:
            return False

    def ActOnTimer(self):
        if self.Active == True:
            self.Pin.Enable()
        else:
            self.Pin.Disable()

    def TimerLoop(self):
        self.GetNewTime()
        self.CheckIfTimerActive()
        self.ActOnTimer()

class Auto():
    def __init__(self):
        #self.ActiveTimers = [[Name, StartHour, EndHour, Pin]]
        self.ActiveTimers = [[]]

    def InitTimers(self):
        try:
            for count in range(1,len(self.ActiveTimers)):
                Name = self.ActiveTimers[count][0]
                StartHour = self.ActiveTimers[count][1]
                EndHour = self.ActiveTimers[count][2]
                Pin = self.ActiveTimers[count][3]
                self.ActiveTimers[count][0] = Timer(Name, StartHour, EndHour, Pin)
                self.ActiveTimers[count][0].TimerLoop()
                Notify.Info("{} Setup.".format(self.ActiveTimers[count][0]))
        except(IndexError):
            print("nopeinit")


    def ViewRunningTimers(self):
        try:
            for count in range(0,len(self.ActiveTimers)):
                print("Timer: {}".format(count))
                print("Name: {}".format(self.ActiveTimers[count][0]))
                print("Starting Hour: {}".format(self.ActiveTimers[count][1]))
                print("Ending Hour: {}".format(self.ActiveTimers[count][2]))
                print("Pin to control: {}".format(self.ActiveTimers[count][3]))
                print()
        except(IndexError):
            print("nope")



    def AddTimer(self):
        while True:
            try:
                Name = input("Please enter the name of the timer: ")
                StartHour = int(input("Please enter the starting hour of the timer: "))
                EndHour = int(input("Please enter the ending hour of the timer: "))
                Pin = input("Please enter the name of the lamp to control: ")
                break
            except(ValueError):
                Notify.Error("Please enter an invalid selection.")
                self.ActiveTimers.append([Name, StartHour, EndHour, Pin])
        self.ViewRunningTimers()
        self.InitTimers()


    def AutoMenu(self):
        print("""
        |------------------------------------------------------------------|
        |                             Auto Menu                            |
        |------------------------------------------------------------------|
        |                                                                  |
        |   [1] View Running Timers                                        |
        |   [2] Add Timer                                                  |
        |   [3] Server Mode                                                |
        |   [4] Back                                                       |
        |                                                                  |
        |------------------------------------------------------------------|
        """)
        while True:
            try:
                menuchoice = int(input("> "))
                if menuchoice not in [1,2,3,4]:
                    Notify.Error("Invalid input.")
                else:
                    break
            except(ValueError):
                Notify.Error("Invalid input.")
        if menuchoice == 1:
            self.ViewRunningTimers()
        elif menuchoice == 2:
            self.AddTimer()
        elif menuchoice == 3:
            self.ServerModeInit()
        elif menuchoice == 4:
            UI.Main()




Auto = Auto()
Status = StatusMode()
Indicator = Indicator()
UI.Main()