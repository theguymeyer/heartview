import threading
import serial
import queue
import tests
from time import sleep
from heartview import detectPeaks
import timeit
import statistics
from serial.tools.list_ports import comports
import k64f
import nucleo

# FRDM_HWID = "0D28:0204" # mbed
FRDM_HWID = "1366:1015" # JLink
NUCLEO_HWID = "0483:374B" # ST-Link

class FrdmSerialThread(threading.Thread):
    def __init__(self, serialPort, inQueue, outQueue):
        super().__init__(target=None)
        self.serialPort = serialPort
        self.inQueue = inQueue
        self.outQueue = outQueue
        self._running = True

    def run(self):
        with serial.Serial(self.serialPort, baudrate=115200, timeout=2) as frdmSerial:
            while self._running:
                try:
                    txData = self.outQueue.get(block=False)
                    frdmSerial.write(txData)
                except queue.Empty:
                    pass
                rxData = frdmSerial.readline()
                if (not rxData or b'\x00' in rxData):
                    continue
                self.inQueue.put(rxData)
    def stop(self):
        self._running = False

class NucleoSerialThread(threading.Thread):
    def __init__(self, serialPort, inQueue, outQueue):
        super().__init__(target=None)
        self.serialPort = serialPort
        self.inQueue = inQueue
        self.outQueue = outQueue
        self._running = True

    def run(self):

        with serial.Serial(self.serialPort, baudrate=115200, timeout=5) as nucleoSerial:
            nucleoSerial.write(b"\x00\x00\x00\x00")
            while self._running:
                try:
                    txData = self.outQueue.get(block=False)
                    nucleoSerial.write(txData)
                except queue.Empty:
                    pass
                while nucleoSerial.read() != b"\xff":
                    pass
                rxData = nucleoSerial.read(4)
                if not rxData:
                    continue
                self.inQueue.put(rxData)
    def stop(self):
        self._running = False

class PeakDetectorThread(threading.Thread):
    def __init__(self, dataQueue, threshQueue, atrEvent, ventEvent):
        super().__init__(target=None)
        self.atrEvent = atrEvent
        self.ventEvent = ventEvent
        self.threshQueue = threshQueue
        self.dataQueue = dataQueue
        self.threshold = 5
        self._running = True

    def run(self):
        while (self._running):
            try:
                self.threshold = self.threshQueue.get_nowait()
            except queue.Empty:
                pass
            # Recieve data from nucleo
            data = self.dataQueue.get()
            peaks = detectPeaks(data, self.threshold)

            if self.atrEvent.isSet():
                if not peaks[0]:
                    self.atrEvent.clear()
                else:
                    continue
            elif self.ventEvent.isSet():
                if not peaks[1]:
                    self.ventEvent.clear()
                else:
                    continue
            if peaks[0]:
                self.atrEvent.set()
            if peaks[1]:
                self.ventEvent.set()
    
    def stop(self):
        self._running = False

def findPorts():
    frdmFound = False
    nucleoFound = False
    nucleoPort = ""
    frdmPort = ""
    while (True):
        for port in comports():
            if FRDM_HWID in port.hwid:
                frdmFound = True
                frdmPort = port.device
            elif NUCLEO_HWID in port.hwid:
                nucleoFound = True
                nucleoPort = port.device
        if (frdmFound and nucleoFound):
            return [nucleoPort, frdmPort]


def main():
    frdmRxQueue = queue.Queue()
    frdmTxQueue = queue.Queue()
    nucleoRxQueue = queue.Queue()
    nucleoTxQueue = queue.Queue()
    threshQueue = queue.Queue()
    atrEvent = threading.Event()
    ventEvent = threading.Event()
    ports = findPorts()
    frdmSerialThread = FrdmSerialThread(ports[1], frdmRxQueue, frdmTxQueue)
    frdmSerialThread.start()
    nucleoSerialThread = NucleoSerialThread(
        ports[0], nucleoRxQueue, nucleoTxQueue
    )
    nucleo.flash("binaries/nucleo.bin")
    nucleoSerialThread.start()
    peakThread = PeakDetectorThread(nucleoRxQueue, threshQueue, atrEvent, ventEvent)
    peakThread.start()
    k64f.flash("binaries/pacing.bin")
    sleep(1)
    AT1_result = tests.AT1(frdmRxQueue, frdmTxQueue).run()
    print(10*"=")
    print(f"Whoami K64F Test: {AT1_result}")
    print(10*"=")
    AT3_result = tests.AT3(nucleoRxQueue, frdmTxQueue, threshQueue, atrEvent, ventEvent).run()
    print(f"Pacing Test (ATR, 5V, 10ms): {AT3_result[0]}")
    print(f"Pacing Test (VENT, 5V, 10ms): {AT3_result[1]}")
    print(f"Pacing Test (ATR, 3V, 5ms): {AT3_result[2]}")
    print(f"Pacing Test (VENT, 3V, 5ms): {AT3_result[3]}")
    print(10*"=")
    k64f.flash("binaries/sensing.bin")
    sleep(1)
    AT4_result = tests.AT4(frdmRxQueue, frdmTxQueue, nucleoTxQueue).run()
    print(f"Sensing Test (ATR, 10ms, 120bpm): {AT4_result[0]}")
    print(f"Sensing Test (VENT, 10ms, 120bpm): {AT4_result[1]}")
    print(10*"=")
    frdmSerialThread.stop()
    nucleoSerialThread.stop()
    peakThread.stop()



if __name__ == "__main__":
    main()
