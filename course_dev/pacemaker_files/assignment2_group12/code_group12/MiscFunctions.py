import serial
import struct
import serial.tools.list_ports
import tkinter as tk
from tkinter import ttk
import json
import os
from Interface import *
import sys
import time

database = {}
pacemaker_values = {}

# Shift value is hardcoded here as a constant for use later in the encrypt/decrypt functions
SHIFT = 2

# Database dump location and upload location is going to be made a constant so it doesnt constantly need to be remade.
DUMP_LOCATION = os.getcwd() + '\database.json'
UPLOAD_LOCATION = os.getcwd() + '\SerialComm.json'

''' DATABASE '''
# Checks if the json file exists
if os.path.exists(DUMP_LOCATION):
    # if it exists, load in that database as the current database.
    with open(DUMP_LOCATION) as f:
        database = json.load(f)
else:
    # Otherwise initialize a new database. 
    database = {}

''' PACEMAKER VALUES '''
# Checks if the json file exists
if os.path.exists(UPLOAD_LOCATION):
    # if it exists, load in that database as the current database.
    with open(UPLOAD_LOCATION) as f:
        pacemaker_values = json.load(f)
else:
    # Otherwise initialize a new database. 
    pacemaker_values = {}

class IO:
    """
    Simple class to do with file i/o and encryptiom/decryption. Consists of three class methods.
    """
    @classmethod
    def encrypt(cls, some_phrase):
        # Given string (user or pass), encrypts using the shift value
        # Used when STORING new user into database

        length = len(some_phrase)
        conv = ""
        for i in range(length):
            conv = conv + chr(ord(some_phrase[i]) + SHIFT)
        return conv

    @classmethod
    def decrypt(cls, some_phrase):
        # Given string (user or pass), decrypts using the shift value
        # Used when READING existing user from database

        length = len(some_phrase)
        conv = ""
        for i in range(length):
            conv = conv + chr(ord(some_phrase[i]) - SHIFT)
        return conv

    @classmethod
    def dump(cls, path, data_dict):
        """
        This function writes the current state of the user database to a json file. Having a local copy is very
        important, since this copy can be written to memory and accessed whether or not the DCM python script is running
        or not, and when the script reboots it remembers who has been registered.

        """
        # 'w+' mode is used to overwrite the previous database with the newest version.
        with open(path, 'w+') as dump_file:
            json.dump(data_dict, dump_file, indent=4, sort_keys=True)

    
def update_info(mode, low, up, AAmp, VAmp, APW, VPW, ASense, VSense, ARP, VRP, MaxSense, PVARP, FAVD, ReTime, RecTime, RespFact, AThresh, user):
    """
    Neatly updates dictionary with pacemaker parameters as per requirements in documentation.
    """

    UpdateMsg = ""            
                
    if low > up:
        low = 50
        UpdateMsg = UpdateMsg + "Lower Rate Limit Fixed to 50ppm \n"

    if MaxSense < low and mode >= 6:
        # in this case we need to tell them, and exit the function
        messagebox.showinfo("Pacemaker Message", "Max Sensor Rate must be greater than or equal to the Lower Limit.")
        return
    pacemaker_values.update({user: {"Mode": mode, "Up_Limit": (up), "Low_Limit": (low), "A_Amp": (AAmp), "V_Amp": (VAmp), "A_PW": (APW), "V_PW": (VPW), "A_Sense": (ASense), "V_Sense": (VSense), "ARP": (ARP), "VRP": (VRP), "Max_Sense": (MaxSense), "PVARP": (PVARP), "FAVD": (FAVD), "ReTime": (ReTime), "RecTime": (RecTime), "RespFact": (RespFact), "AThresh": (AThresh)}})
    IO.dump(UPLOAD_LOCATION, pacemaker_values)
    # Serial Communication
    communicate_parameters(mode, low, up, AAmp, VAmp, APW, VPW, ASense, VSense, ARP, VRP, MaxSense, FAVD, ReTime, RecTime, RespFact, AThresh)
    UpdateMsg = UpdateMsg + "Pacemaker Values Updated Successfully"
    messagebox.showinfo("Pacemaker Message", UpdateMsg)



def _to_bytes(mode, low, up, Aamp, Vamp, Apw, Vpw, Asense, Vsense, ARP, VRP, MSR, FAVD, RE, REC, RES, AT):
    """
    Takes parameters and packs them into a bytes array for serial comms.
    Returns said bytes array.
    """

    # Something like this seems to be the proper thing to do. We'll have to see
    return struct.pack('<BHHddHHddHHHHHBBHB', mode, low, up, Aamp, Vamp, Apw, Vpw, Asense, Vsense, ARP, VRP, FAVD, RE, REC, RES, AT, MSR, 255)
    # DCM to Board= FF, Board to DCM = 00!

baud_rate = 115200


'''
Serial object used for communication. The port value must match with
the device running the software. For example, COM8 was used in development
but would need to be switched for a different device
'''

# WARNING: the port in the below serial object needs to be changed for each user. It may not work right away.
board = serial.Serial(
                        port='COM5',
                        baudrate=baud_rate,
                        parity=serial.PARITY_NONE,
                        bytesize=8
                    )


def communicate_parameters(mode, low, up, AAmp, VAmp, APW, VPW, ASense, VSense, ARP, VRP, MaxSense, FAVD, ReTime, RecTime, RespFact, AThresh):
    """
    This function takes the given inputs and prepares them for serial communication.
    Makes a local copy of the data being sent, so it can compare it to the values the board
    receives. If an discrepancy is detected, the user is notified.
    """
    good_params = [mode, low, up, AAmp, VAmp, APW, VPW, ASense, VSense, ARP, VRP, FAVD, ReTime, RecTime, RespFact, AThresh, MaxSense]
    try:
        data = _to_bytes(mode, low, up, AAmp, VAmp, APW, VPW, ASense, VSense, ARP, VRP, MaxSense, FAVD, ReTime, RecTime, RespFact, AThresh)

        board.write(data)

        i = 0  # iteration variable for parallel iteration!
        transmission_ok = True  # We will assume for the implementation that transmission will go OK until it doesn't!
        board_params = struct.unpack('<BHHddHHddHHHHHBBH', board.read(55))

        """
        Here we will iterate through the original parameters and the parameters we recieve from the microcontroller
        to make sure that they are one-to-one and have therefore transmitted correctly! 
        """

        for value in board_params:
            if value != good_params[i]:
                # In this case we have an issue with the transmission of the values!
                messagebox.showerror("Communication Error", "A parameter was not transmitted correctly. The difference is shown here: %d, and %d" % (value, good_params[i]))
                transmission_ok = False # error occurred so it changes to False.
            
            # No issue in this case so incremenint by 1.
            i = i + 1

        if transmission_ok:
            messagebox.showinfo("Communication OK", "All parameters were transmitted properly")

    except KeyError as e:
        messagebox.showinfo("Error", "Something went critically wrong: " + str(e))


   



