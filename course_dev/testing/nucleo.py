import pyocd
from pyocd.probe.stlink_probe import StlinkProbe
from pyocd.flash.file_programmer import FileProgrammer
from pyocd.core.session import Session

def flash(binary):
    probes = StlinkProbe.get_all_connected_probes()
    for probe in probes:
        if "F446RE" in probe.description:
            try:
                with Session(probe) as session:
                    board = session.board
                    target = board.target
                    # Load firmware into device.
                    FileProgrammer(session).program(binary)
                    # Reset, run.
                    target.reset()
            except Exception as e:
                print(e)