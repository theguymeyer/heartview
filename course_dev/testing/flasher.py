from pyocd.probe.cmsis_dap_probe import CMSISDAPProbe
from pyocd.probe.stlink_probe import StlinkProbe
from pyocd.flash.file_programmer import FileProgrammer
from pyocd.core.session import Session

def flash_target(probe, binary, progressCallback=None):
    print(f"Flashing {binary} to {probe.description}")
    try:
        with Session(probe) as session:
            board = session.board
            target = board.target
            # Load firmware into device.
            FileProgrammer(session, progress=progressCallback).program(binary)
            # Reset, run.
            target.reset()

    except Exception as e:
        print(f"Error: {e}")


def find_probe(target_name):
    probes = CMSISDAPProbe.get_all_connected_probes()
    probes += StlinkProbe.get_all_connected_probes()
    for probe in probes:
        if target_name in probe.description:
            return probe
    return None

def main():
    # flash_target(find_probe("K64F"), "frdm.bin")
    flash_target(find_probe("F446RE"), "nucleo.bin")

if __name__ == "__main__":
    main()
    