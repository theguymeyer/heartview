import pylink

def flash(binary):
    jlink = pylink.JLink()

    jlink.open(serial_no=123456)
    jlink.connect("MK64FN1M0xxx12")
    jlink.flash_file(binary, 0x0)
    jlink.reset()
