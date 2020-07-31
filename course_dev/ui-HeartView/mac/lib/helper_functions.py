
class Helpers():


    def __init__(self):

        # adc to volts useful parameters
        self.adcLow = -5.0       # volts
        self.adcHigh = 5.0      # volts
        self.adcRes = 255.0     # quantization
    
    # maps a range of adc values to millivolts
    # RANGE: 0 - 255
    # dType: Type of data point  (useful for correct scaling)
    #   .. true => pacemaker
    #   .. false => natural 
    def adc2volts(self, adc_reading, dType):
        if (dType):
            return (((self.adcHigh - self.adcLow)/(self.adcRes)) * int.from_bytes(adc_reading, 'little') + self.adcLow) * 1000
        else:
            return (((self.adcHigh)/(self.adcRes)) * int.from_bytes(adc_reading, 'little')) * 1000