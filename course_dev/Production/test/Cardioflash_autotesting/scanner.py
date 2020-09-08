import threading
from time import sleep
import flasher
from serial.tools.list_ports import comports


FRDM_HWID = "0D28:0204"
NUCLEO_HWID = "0483:374B"


class DeviceScannerThread (threading.Thread):
    def __init__(self, status_frame, flashQueue, nucleoProgressQueue, frdmProgressQueue, nucleoBinary, frdmBinary):
        super(DeviceScannerThread, self).__init__(target=None)
        self.nucleoProbe = None
        self.frdmProbe = None
        self.nucleoBinary = nucleoBinary
        self.frdmBinary = frdmBinary
        self.status_frame = status_frame
        self.flashQueue = flashQueue
        self.nucleoProgressQueue = nucleoProgressQueue
        self.frdmProgressQueue = frdmProgressQueue

    def flash(self):
        try:
            if self.nucleoProbe:
                flasher.flash_target(self.nucleoProbe, self.nucleoBinary,
                                     lambda progress: self.updateNucleoProgress(progress))
            if self.frdmProbe:
                flasher.flash_target(self.frdmProbe, self.frdmBinary,
                                     lambda progress: self.updateFrdmProgress(progress))
        except Exception as e:
            print(f"Exception: {e}")

    def updateNucleoProgress(self, progress):
        self.nucleoProgressQueue.put(progress)
        self.status_frame.updateProgress()

    def updateFrdmProgress(self, progress):
        try:
            self.frdmProgressQueue.put(progress)
            self.status_frame.updateProgress()
        except Exception as e:
            print(f"Exception: {e}")

    def run(self):
        while(1):
            try:
                binaries = self.flashQueue.get_nowait()
                self.nucleoBinary = binaries[0]
                self.frdmBinary = binaries[1]
                self.flash()
            except:
                pass
            self.nucleoProbe = flasher.find_probe("F446RE")
            self.frdmProbe = flasher.find_probe("K64F")
            nucleoUUID = ""
            frdmUUID = ""
            if (self.nucleoProbe):
                nucleoUUID = self.nucleoProbe.unique_id
            if (self.frdmProbe):
                frdmUUID = self.frdmProbe.unique_id
            self.status_frame.update_status(nucleoUUID, frdmUUID)
            sleep(0.1)


class PortScanner (threading.Thread):
    def __init__(self, mainFrame):
        super(PortScanner, self).__init__(target=None)
        self.frdmPort = None
        self.nucleoPort = None
        self.mainFrame = mainFrame

    def run(self):
        while (True):
            frdmFound = False
            nucleoFound = False
            prevStatus = [self.nucleoPort, self.frdmPort]
            for port in comports():
                if FRDM_HWID in port.hwid:
                    frdmFound = True
                    self.frdmPort = port.device
                elif NUCLEO_HWID in port.hwid:
                    nucleoFound = True
                    self.nucleoPort = port.device
            if (not frdmFound):
                self.frdmPort = ""
            if (not nucleoFound):
                self.nucleoPort = ""
            if prevStatus != [self.nucleoPort, self.frdmPort]:
                self.mainFrame.updatePorts(self.nucleoPort, self.frdmPort)
            sleep(0.1)
