# Shield Modifications

This document specifies the alterations needed for the Pacemaker shield (shield A). The current design of the shield can be found under,
        >> design >> rev2

## Mod 1 - Pin Swaps

The current revision (rev2) of the shield contains incorrect pin routing on certain pins. The corrections are outlined in "pin_swap_mod.png"

## Mod 2 - Replacing Connector X1

The goal is to provide a solution that will be allow for easy connections of jumper wires.
Note that each pin is connected twice to the board, a single PCB connection is **assumed** to suffice.

Instructions:
- update the BOM to include female header pins 
- ensure that the PCB matches the updated pins

## Mod 3 - Replacing Connector SV1

The current pins are incompatible with standard jumper wires. As such this part is to be changed in BOM to include 0.1" male header pins that fit female jumper wires connectors. 
