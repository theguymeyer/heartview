import queue
from heartview import detectPeaks
from time import sleep


class AT1:
    def __init__(self, frdmRxQueue, frdmTxQueue):
        self.name = "K64F WhoAmI"
        self.rxQueue = frdmRxQueue
        self.txQueue = frdmTxQueue

    def run(self):
        self.txQueue.put([0, 0, 0])
        try:
            rxData = self.rxQueue.get(timeout=2)  # Timesout after 2 seconds
            return True if rxData == b'K64F\n' else False
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
    def __init__(self, nucleoRxQueue, frdmTxQueue, threshQueue, peaksQueue):
        self.name = "K64F Pacing"
        self.rxQueue = nucleoRxQueue
        self.txQueue = frdmTxQueue
        self.threshQueue = threshQueue
        self.peaksQueue = peaksQueue
        self.results = []

    def pace(self, chamber, amplitude, pulseWidth):
        chamber = 1 if chamber == "ATR" else 2
        self.txQueue.put([chamber, amplitude, pulseWidth])

    def run(self):

        # ATR, 5V, 10ms
        sleep(1)
        self.threshQueue.put(5)
        self.pace("ATR", 5, 10)
        try:
            peak = self.peaksQueue.get(timeout=1)
            if (peak == "ATR"):
                self.results.append(True)
            else:
                self.results.append(False)
        except queue.Empty:
            self.results.append(False)

        sleep(1)
        # VENT, 5V, 10ms
        self.pace("VENT", 5, 10)
        try:
            peak=self.peaksQueue.get(timeout=1)
            if (peak == "VENT"):
                self.results.append(True)
            else:
                self.results.append(False)
        except queue.Empty:
            self.results.append(False)

        # ATR, 2V, 1ms
        # sleep(1)
        # self.threshQueue.put(2)
        # self.pace("ATR", 2, 1)
        # try:
        #     peak = self.peaksQueue.get(timeout=1)
        #     if (peak == "ATR"):
        #         self.results.append(True)
        #     else:
        #         self.results.append(False)
        # except queue.Empty:
        #     self.results.append(False)

        # sleep(1)
        # # VENT, 2V, 1ms
        # self.threshQueue.put(2)
        # self.pace("VENT", 2, 1)
        # try:
        #     peak = self.peaksQueue.get(timeout=1)
        #     if (peak == "VENT"):
        #         self.results.append(True)
        #     else:
        #         self.results.append(False)
        # except queue.Empty:
        #     self.results.append(False)

        return self.results
