
class Helpers():


    def __init__(self):

        # adc to volts useful parameters
        self.adcLow = 0.0       # volts
        self.adcHigh = 5.0      # volts
        self.adcRes = 255.0     # quantization
    
    # maps a range of adc values to millivolts
    # RANGE: 0 - 255
    def adc2volts(self, adc_reading):
        return ((self.adcHigh - self.adcLow)/(self.adcRes) * int.from_bytes(adc_reading, 'little')) * 1000 