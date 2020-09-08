import threading
import serial
import queue
import tests
from time import sleep
from heartview import detectPeaks
import timeit


class FrdmSerialThread (threading.Thread):
    def __init__(self, serialPort, inQueue, outQueue):
        super().__init__(target=None)
        self.serialPort = serialPort
        self.inQueue = inQueue
        self.outQueue = outQueue
        self._running = True

    def run(self):
        with serial.Serial(self.serialPort,
                           baudrate=115200, timeout=2) as frdmSerial:
            while (self._running):
                try:
                    txData = self.outQueue.get(block=False)
                    frdmSerial.write(txData)
                except queue.Empty:
                    pass
                rxData = frdmSerial.readline()
                if not rxData:
                    continue
                self.inQueue.put(rxData)


class NucleoSerialThread (threading.Thread):
    def __init__(self, serialPort, inQueue, outQueue):
        super().__init__(target=None)
        self.serialPort = serialPort
        self.inQueue = inQueue
        self.outQueue = outQueue
        self._running = True

    def run(self):

        with serial.Serial(self.serialPort,
                           baudrate=115200, timeout=5) as nucleoSerial:
            nucleoSerial.write(b'\x80\x80\x00\x00')
            while (self._running):
                try:
                    txData = self.outQueue.get(block=False)
                    nucleoSerial.write(txData)
                except queue.Empty:
                    pass
                while nucleoSerial.read() != b'\xff':
                    pass
                rxData = nucleoSerial.read(4)
                if not rxData:
                    continue
                self.inQueue.put(rxData)


class PeakDetectorThread (threading.Thread):
    def __init__(self, dataQueue, threshQueue, peaksQueue):
        super().__init__(target=None)
        self.dataQueue = dataQueue
        self.threshQueue = threshQueue
        self.peaksQueue = peaksQueue
        self.threshold = 5

    def run(self):
        while True:
            try:
                self.threshold = self.threshQueue.get_nowait()
            except queue.Empty:
                pass
            data = self.dataQueue.get()
            peaks = detectPeaks(data, self.threshold)
            if peaks[0]:
                self.peaksQueue.put("ATR")
                while(detectPeaks(data, self.threshold)[0]):
                    data = self.dataQueue.get()
                    pass
            elif peaks[1]:
                self.peaksQueue.put("VENT")
                while(detectPeaks(data, self.threshold)[1]):
                    data = self.dataQueue.get()
                    pass


def main():
    frdmRxQueue = queue.Queue()
    frdmTxQueue = queue.Queue()
    nucleoRxQueue = queue.Queue()
    nucleoTxQueue = queue.Queue()
    threshQueue = queue.Queue()
    peaksQueue = queue.Queue()
    frdmWhoAmI = tests.AT1(frdmRxQueue, frdmTxQueue)
    frdmSerialThread = FrdmSerialThread("/dev/ttyACM0",
                                        frdmRxQueue, frdmTxQueue)
    frdmSerialThread.start()
    nucleoSerialThread = NucleoSerialThread("/dev/ttyACM1",
                                            nucleoRxQueue, nucleoTxQueue)
    nucleoSerialThread.start()
    PeakDetectorThread(nucleoRxQueue, threshQueue, peaksQueue).start()
    print(frdmWhoAmI.run())
    while True:
        print(tests.AT3(nucleoRxQueue, frdmTxQueue,
                  threshQueue, peaksQueue).run())


if __name__ == "__main__":
    main()
    input()
