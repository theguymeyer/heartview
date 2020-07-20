# Documentation for the testing controller shield

The model is developed using LTspice with imported models. No model was found for the TLE2426CDR Rail Splitter chip so the model does not currently compile

The most up-to-date model is titled "nucleo_shield_heart_interface_rev2.asc"

### Notes on In Amp circuitry

- This Circuit was designed from information in this document (p.5-3 was especially helpful) (https://www.analog.com/media/en/training-seminars/design-handbooks/designers-guide-instrument-amps-complete.pdf)
- Desired Gain: 1/2
- Vcm = GND // the middle of the expected input dynamic range 
- note... the in-amp’s input buffers will need to swing both positive and negative with respect to ground
- Vref = 2.5V //  centered on the expected output dynamic range
- "A good guideline is to keep IBR < 10 mV" (p.5-3)
- Need to use "1% metal film resistors"

### Notes on pulse generation circuitry

Pulse Characteristics:
 - 5V square pulse
 - duration ranges from 100 us to 5 ms (according to PACEMAKER doc)

**IMPORTANT** The onboard toggle switch found on the pacemaker shield MUST be placed to 'x100' in order to comply with the pulse characteristics
 
Note: Recent discoveries in pacemaker shield show that the 
pulse is substantially filtered when nearing 3ms PW or below
