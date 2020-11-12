import math
ADC_LOW = -5.0       # volts
ADC_HIGH = 5.0      # volts
ADC_RES = 255.0     # quantization


def detectPeaks(serialData, threshold, tolerance=1):
    def paceADC(reading): return (
        ((ADC_HIGH - ADC_LOW)/(ADC_RES)) * (reading) + ADC_LOW)

    return [math.isclose(
        paceADC(serialData[0]), threshold, abs_tol=tolerance), math.isclose(
        paceADC(serialData[1]), threshold, abs_tol=tolerance)]
