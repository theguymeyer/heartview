import queue
from heartview import detectPeaks
import threading


class AT1:
    def __init__(self, frdmRxQueue, frdmTxQueue):
        self.name = "K64F WhoAmI"
        self.rxQueue = frdmRxQueue
        self.txQueue = frdmTxQueue

    def run(self):
        self.txQueue.put([0, 0, 0])
        try:
            rxData = self.rxQueue.get(timeout=5)  # Timesout after 2 seconds
            return True if rxData == b"K64F\r\n" else False
        except queue.Empty:
            print("No Data Recieved")
            return False


class AT2:
    def __init__(self, nucleoRxQueue, nucleoTxQueue):
        self.name = "F446RE WhoAmI"
        self.rxQueue = nucleoRxQueue
        self.txQueue = nucleoTxQueue

    def run(self):
        self.txQueue.put([0, 0, 0, 0])
        try:
            rxData = self.rxQueue.get(timeout=2)  # Timesout after 2 seconds
            return True if rxData == "F446RE" else False
        except queue.Empty:
            print("No Data Recieved")
            return False


class AT3:
    def __init__(self, nucleoRxQueue, frdmTxQueue, threshQueue, atrEvent, ventEvent):
        self.name = "K64F Pacing"
        self.rxQueue = nucleoRxQueue
        self.txQueue = frdmTxQueue
        self.threshQueue = threshQueue
        self.atrEvent = atrEvent
        self.ventEvent = ventEvent
        self.results = []

    def pace(self, chamber, amplitude, pulseWidth):
        chamber = 1 if chamber == "ATR" else 2
        self.txQueue.put([chamber, amplitude, pulseWidth])

    def run(self):
        # ATR, 5V, 10ms
        self.threshQueue.put(5)
        self.pace("ATR", 5, 10)
        while self.ventEvent.isSet():
            pass
        self.results.append(self.atrEvent.wait(timeout=5))

        # VENT, 5V, 10ms
        self.pace("VENT", 5, 10)
        while self.atrEvent.isSet():
            pass
        self.results.append(self.ventEvent.wait(timeout=5))

        # ATR, 3V, 5ms
        self.threshQueue.put(3)
        self.pace("ATR", 3, 5)
        while self.ventEvent.isSet():
            pass
        self.results.append(self.atrEvent.wait(timeout=5))

        # VENT, 3V, 5ms
        self.pace("VENT", 3, 5)
        while self.atrEvent.isSet():
            pass
        self.results.append(self.ventEvent.wait(timeout=5))

        return self.results


class AT4:
    def __init__(self, frdmRxQueue, frdmTxQueue, nucleoTxQueue):
        self.name = "K64F Sensing"
        self.rxQueue = frdmRxQueue
        self.txQueue = nucleoTxQueue
        self.sensingQueue = frdmTxQueue
        self.results = []

    def pace(self, chamber, pulseWidth, rate):
        if chamber == "ATR":
            self.txQueue.put([pulseWidth, 0, rate, 120])
        else:
            self.txQueue.put([0, pulseWidth, rate, 120])

    def run(self):
        self.pace("ATR", 10, 120)
        try:
            rxData = self.rxQueue.get(timeout=10)  # Timesout after 2 seconds
            self.results.append(True if rxData == b'ATR\r\n' else False)
        except queue.Empty:
            print("No Data Recieved")
            self.results.append(False)
        
        self.pace("VENT", 10, 120)
        try:
            rxData = self.rxQueue.get(timeout=5)  # Timesout after 2 seconds
            self.results.append(True if rxData == b'VENT\r\n' else False)
        except queue.Empty:
            print("No Data Recieved")
            self.results.append(False)

        return self.results
