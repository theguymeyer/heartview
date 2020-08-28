import tkinter as tk
from tkinter import ttk
import json
import os
from tkinter import messagebox
from MiscFunctions import *

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

style.use('fivethirtyeight')
UserID = "UserID"
AEgram = 0
VEgram = 0

''' ------------------------------------------------------ '''
def _create_user(username, password, frame_class):
    """
    This function takes the desired username and password input into the two text boxes in the GUI and does some
    operations.
    It checks it against the existing database, which must be limited to 20 users, to see if it exists, and if not, will
    input it into the database.
    Also takes a frame_class
    """

    global UserID
    # Encrypt both the password and the username and update the database.
    en_user = IO.encrypt(str(username.get()))
    UserID = str(username.get())
    en_pass = IO.encrypt(str(password.get()))

    """
    Conditional will check our three conditions for adding to database: 
    less than 10 entries 
    and the user doesnt exist,
    and we have a valid password.
    """
    if len(database.items()) < 10 and database.get(en_user) is None and len(
            en_pass) > 0 and len(en_user) > 0:  # added no password case
        database.update({en_user: en_pass})
        IO.dump(DUMP_LOCATION, database)
        # We passed an object through (master in this case)
        frame_class._switch_frame(_Menu)
    elif database.get(en_user):
        messagebox.showinfo("Username already exists.", "Please login with this user or attempt to create a new one.")
        return
    elif len(en_user) == 0:
        messagebox.showinfo("Please enter username", "Enter a valid username.")
    elif len(en_pass) == 0:
        messagebox.showinfo("Please enter password", "Enter a valid password.")
    else:
        messagebox.showinfo("Database is full", "The database cannot accept any more users.")


def _login_test(username, password, frame_class):
    """Function takes text-variable version of username and password, as well as frame class"""

    global UserID
    # Like in the create user function we will be using the encoded version
    en_user = IO.encrypt(str(username.get()))
    UserID = str(username.get())
    en_pass = IO.encrypt(str(password.get()))

    if (len(en_user) == 0) or (len(en_pass) == 0):
        messagebox.showinfo("Invalid credentials", "Either your username or password are invalid, try again.")
    if database.get(en_user) != en_pass:
        messagebox.showinfo("Wrong Password", "Enter a valid password")
    elif database.get(en_user) == en_pass:
        frame_class._switch_frame(_Menu)
    else:
        messagebox.showinfo("User does not exist", "This user does not exist in the database, try again.")

def _egramSwitch(value):
    """
    Included in the program, but doesn't function like a proper egram. Determines which Egram data set to display
    and uses _animate function to display the graph. Changes global variables that will be used in _animate
    """
    global AEgram
    global VEgram
    style.use('fivethirtyeight')
    global fig
    fig = plt.figure()
    if (value == 1):
        AEgram = 1
        VEgram = 0
        ani = animation.FuncAnimation(fig, _animate, interval=100)
        plt.show()
    elif (value == 2):
        AEgram = 0
        VEgram = 1
        ani = animation.FuncAnimation(fig, _animate, interval=100)
        plt.show()
    elif (value == 3):
        AEgram = 1
        VEgram = 1
        ani = animation.FuncAnimation(fig, _animate, interval=100)
        plt.show()
    else:
        messagebox.showinfo("OOPS", "Something went wrong.")

        
def _animate(i):
    """
    Depending on the global variables set in _egramSwitch, displays the data from the text files. Egrams aren't fully implemented
    in the program, but this function is the beginning of including the functionality. In the future, a more practical method will
    be used for reading the values.
    """
    global fig
    global AEgram
    global VEgram
    xA = []
    yA = []
    xV = []
    yV = []
    if (AEgram == 1):
        ax1 = fig.add_subplot(1,1,1)
        graph_data = open('Atrium Values.txt','r').read()
        lines = graph_data.split('\n')
        for line in lines:
            if len(line) > 1:
                x, y = line.split(',')
                xA.append(float(x))
                yA.append(float(y))
                
    if (VEgram == 1):
        ax1 = fig.add_subplot(1,1,1)
        second_data = open('Ventricle Values.txt','r').read()
        values = second_data.split('\n')
        for value in values:
            if len(value) > 1:
                x, y = value.split(',')
                xV.append(float
                          (x))
                yV.append(float(y))
                
    ax1.clear()
    ax1.plot(xA, yA, xV, yV)

''' ============================================================= '''


class DCM(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.title("Pacemaker Interface")
        self._switch_frame(_StartUp)

    def _switch_frame(self, frame_class):
        """
        Destroys current frame and replaces it with a new one.
        """
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


class _StartUp(tk.Frame):
    def __init__(self, master):
        """ The first window that the user sees - the Welcome screen """
        tk.Frame.__init__(self, master)
        master.resizable(False, False)
        tk.Label(self, text="Welcome").pack()
        tk.Button(self, text="Login",
                  command=lambda: master._switch_frame(_Login)).pack(padx=10, pady=10)
        tk.Button(self, text="Create User",
                  command=lambda: master._switch_frame(_CreateUser)).pack(padx=10, pady=10)


class _Login(tk.Frame):
    def __init__(self, master):
        """ Login Window """
        v1 = tk.StringVar()
        v2 = tk.StringVar()
        login = 0
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Enter your credentials").pack(side="top", fill="x", pady=10)
        tk.Label(self, text="Enter Username").pack()
        tk.Entry(self, textvariable=v1).pack()
        tk.Label(self, text="Enter Password").pack()
        tk.Entry(self, show="*", textvariable=v2).pack(padx=5)
        tk.Button(self, text="Submit", command=lambda: _login_test(v1, v2, master)).pack()
        tk.Button(self, text="Return to start page",
                  command=lambda: master._switch_frame(_StartUp)).pack()
        if login == 1:
            master._switch_frame(_Menu)


class _CreateUser(tk.Frame):
    def __init__(self, master):
        """ Create User Window """
        v1 = tk.StringVar()
        v2 = tk.StringVar()
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Create a new user").pack(side="top", fill="x", padx=40, pady=10)
        tk.Label(self, text="Enter Username").pack()
        tk.Entry(self, textvariable=v1).pack()
        tk.Label(self, text="Enter Password").pack()
        tk.Entry(self, textvariable=v2).pack()
        tk.Button(self, text="Create",
                  command=lambda: _create_user(v1, v2, master)).pack()
        tk.Button(self, text="Return to start page",
                  command=lambda: master._switch_frame(_StartUp)).pack()
        

class _Menu(tk.Frame):
    def __init__(self, master):
        """ The Main Interface of the Program, Interactive Parameter Values """
        tk.Frame.__init__(self, master)
        master.resizable(False, False)      
        tabControl = ttk.Notebook(master)
        AOOTab = ttk.Frame(tabControl)
        VOOTab = ttk.Frame(tabControl)
        AAITab = ttk.Frame(tabControl)
        VVITab = ttk.Frame(tabControl)
        DOOTab = ttk.Frame(tabControl)
        AOORTab = ttk.Frame(tabControl)
        VOORTab = ttk.Frame(tabControl)
        AAIRTab = ttk.Frame(tabControl)
        VVIRTab = ttk.Frame(tabControl)
        DOORTab = ttk.Frame(tabControl)
        DDDRTab = ttk.Frame(tabControl)
        tabControl.add(AOOTab, text='AOO')
        tabControl.add(VOOTab, text='VOO')
        tabControl.add(AAITab, text='AAI')
        tabControl.add(VVITab, text='VVI')
        tabControl.add(DOOTab, text='DOO')
        tabControl.add(AOORTab, text='AOOR')
        tabControl.add(VOORTab, text='VOOR')
        tabControl.add(AAIRTab, text='AAIR')
        tabControl.add(VVIRTab, text='VVIR')
        tabControl.add(DOORTab, text='DOOR')
        tabControl.add(DDDRTab, text='DDDR')
        tabControl.pack(expand=1, side="top")
        
        # AOO
        row1 = ttk.Frame(AOOTab)
        row1.pack()
        row2 = ttk.Frame(AOOTab)
        row2.pack()
        row3 = ttk.Frame(AOOTab)
        row3.pack()
        row4 = ttk.Frame(AOOTab)
        row4.pack()
        row5 = ttk.Frame(AOOTab)
        row5.pack()
        row6 = ttk.Frame(AOOTab)
        row6.pack()
        tk.Label(row1, text="Lower Rate Limit (ppm)").pack(side="left", padx=5, pady=5)
        AOOLRL = tk.Scale(row1, from_=50, to=175, length=600, tickinterval=15, orient=tk.HORIZONTAL)
        AOOLRL.pack(side="left", padx=5, pady=5)
        tk.Label(row2, text="Upper Rate Limit (ppm)").pack(side="left", padx=5, pady=5)
        AOOURL = tk.Scale(row2, from_=75, to=175, length=600, tickinterval=15, orient=tk.HORIZONTAL)
        AOOURL.pack(side="left", padx=5, pady=5)
        tk.Label(row3, text="Atrial Amplitude(V)").pack(side="left", padx=15, pady=5)
        AOOAA = tk.Scale(row3, from_=0.5, to=5, resolution=0.5, length=600, tickinterval=0.5, orient=tk.HORIZONTAL)
        AOOAA.pack(side="left", padx=5, pady=5)
        tk.Label(row4, text="Atrial Pulse Width (ms)").pack(side="left", padx=6, pady=5)
        AOOPW = tk.Scale(row4, from_=1, to=10, length=600, tickinterval=1, orient=tk.HORIZONTAL)
        AOOPW.pack(side="left", padx=5, pady=5)
        tk.Button(row5, text="Submit", command=lambda:
                  update_info(1, AOOLRL.get(), AOOURL.get(), AOOAA.get(), 3, AOOPW.get(), 10, 2.75, 2.75, 300, 300, 120, 0, 150, 4, 10, 8, 2, UserID)).pack(side="bottom", pady=5)
        tk.Label(row6, text="User: " + UserID).pack(side="left", padx=5, pady=5)
        tk.Label(row6, text=" ").pack(side="left", padx=180, pady=5)
        tk.Button(row6, text="Atrium Egram", command=lambda:
                  _egramSwitch(1)).pack(side="left", pady=5)
        tk.Button(row6, text="Ventricle Egram", command=lambda:
                  _egramSwitch(2)).pack(side="left", pady=5)
        tk.Button(row6, text="Dual Egram", command=lambda:
                  _egramSwitch(3)).pack(side="left", pady=5)

        # VOO
        row1 = ttk.Frame(VOOTab)
        row1.pack()
        row2 = ttk.Frame(VOOTab)
        row2.pack()
        row3 = ttk.Frame(VOOTab)
        row3.pack()
        row4 = ttk.Frame(VOOTab)
        row4.pack()
        row5 = ttk.Frame(VOOTab)
        row5.pack()
        row6 = ttk.Frame(VOOTab)
        row6.pack()
        tk.Label(row1, text="Lower Rate Limit (ppm)").pack(side="left", padx=22, pady=5)
        VOOLRL = tk.Scale(row1, from_=50, to=175, length=600, tickinterval=15, orient=tk.HORIZONTAL)
        VOOLRL.pack(side="left", padx=5, pady=5)
        tk.Label(row2, text="Upper Rate Limit (ppm)").pack(side="left", padx=22, pady=5)
        VOOURL = tk.Scale(row2, from_=75, to=175, length=600, tickinterval=15, orient=tk.HORIZONTAL)
        VOOURL.pack(side="left", padx=5, pady=5)
        tk.Label(row3, text="Ventricular Amplitude (V)").pack(side="left", padx=17, pady=5)
        VOOVA = tk.Scale(row3, from_=0.5, to=5, resolution=0.5, length=600, tickinterval=0.5, orient=tk.HORIZONTAL)
        VOOVA.pack(side="left", padx=5, pady=5)
        tk.Label(row4, text="Ventricular Pulse Width (ms)").pack(side="left", padx=10, pady=5)
        VOOPW = tk.Scale(row4, from_=1, to=10, length=600, tickinterval=1, orient=tk.HORIZONTAL)
        VOOPW.pack(side="left", padx=5, pady=5)
        tk.Button(row5, text="Submit", command=lambda:
                  update_info(2, VOOLRL.get(), VOOURL.get(), 3, VOOVA.get(), 10, VOOPW.get(), 2.75, 2.75, 300, 300, 120, 0, 150, 4, 10, 8, 2, UserID)).pack(side="bottom", pady=5)
        tk.Label(row6, text="User: " + UserID).pack(side="left", padx=0, pady=5)
        tk.Label(row6, text=" ").pack(side="left", padx=180, pady=5)
        tk.Button(row6, text="Atrium Egram", command=lambda:
                  _egramSwitch(1)).pack(side="left", pady=5)
        tk.Button(row6, text="Ventricle Egram", command=lambda:
                  _egramSwitch(2)).pack(side="left", pady=5)
        tk.Button(row6, text="Dual Egram", command=lambda:
                  _egramSwitch(3)).pack(side="left", pady=5)

        # AAI
        row1 = ttk.Frame(AAITab)
        row1.pack()
        row2 = ttk.Frame(AAITab)
        row2.pack()
        row3 = ttk.Frame(AAITab)
        row3.pack()
        row4 = ttk.Frame(AAITab)
        row4.pack()
        row5 = ttk.Frame(AAITab)
        row5.pack()
        row6 = ttk.Frame(AAITab)
        row6.pack()
        row7 = ttk.Frame(AAITab)
        row7.pack()
        row8 = ttk.Frame(AAITab)
        row8.pack()
        tk.Label(row1, text="Lower Rate Limit (ppm)").pack(side="left", padx=11, pady=5)
        AAILRL = tk.Scale(row1, from_=50, to=175, length=600, tickinterval=15, orient=tk.HORIZONTAL)
        AAILRL.pack(side="left", padx=5, pady=5)
        tk.Label(row2, text="Upper Rate Limit (ppm)").pack(side="left", padx=11, pady=5)
        AAIURL = tk.Scale(row2, from_=75, to=175, length=600, tickinterval=15, orient=tk.HORIZONTAL)
        AAIURL.pack(side="left", padx=5, pady=5)
        tk.Label(row3, text="Atrial Amplitude (V)").pack(side="left", padx=21, pady=5)
        AAIAA = tk.Scale(row3, from_=0.5, to=5, resolution=0.5, length=600, tickinterval=0.5, orient=tk.HORIZONTAL)
        AAIAA.pack(side="left", padx=5, pady=5)
        tk.Label(row4, text="Atrial Pulse Width (ms)").pack(side="left", padx=13, pady=5)
        AAIPW = tk.Scale(row4, from_=1, to=10, length=600, tickinterval=1, orient=tk.HORIZONTAL)
        AAIPW.pack(side="left", padx=5, pady=5)
        tk.Label(row5, text="Atrial Sense Threshold (V) ").pack(side="left", padx=0, pady=5)
        AAIAS = tk.Scale(row5, from_=0.5, to=3.3, resolution=0.1, length=600, tickinterval=0.3, orient=tk.HORIZONTAL)
        AAIAS.pack(side="left", padx=0, pady=5)
        tk.Label(row6, text="ARP (ms)").pack(side="left", padx=49, pady=5)
        AAIARP = tk.Scale(row6, from_=150, to=500, length=600, tickinterval=20, orient=tk.HORIZONTAL)
        AAIARP.pack(side="left", padx=5, pady=5)
        tk.Button(row7, text="Submit", command=lambda:
                  update_info(3, AAILRL.get(), AAIURL.get(), AAIAA.get(), 3, AAIPW.get(), 10, AAIAS.get(), 2.75, AAIARP.get(), 300, 120, 0, 150, 4, 10, 8, 2, UserID)).pack(side="bottom", pady=5)
        tk.Label(row8, text="User: " + UserID).pack(side="left", padx=0, pady=5)
        tk.Label(row8, text=" ").pack(side="left", padx=180, pady=5)
        tk.Button(row8, text="Atrium Egram", command=lambda:
                  _egramSwitch(1)).pack(side="left", pady=5)
        tk.Button(row8, text="Ventricle Egram", command=lambda:
                  _egramSwitch(2)).pack(side="left", pady=5)
        tk.Button(row8, text="Dual Egram", command=lambda:
                  _egramSwitch(3)).pack(side="left", pady=5)
        
        # VVI
        row1 = ttk.Frame(VVITab)
        row1.pack()
        row2 = ttk.Frame(VVITab)
        row2.pack()
        row3 = ttk.Frame(VVITab)
        row3.pack()
        row4 = ttk.Frame(VVITab)
        row4.pack()
        row5 = ttk.Frame(VVITab)
        row5.pack()
        row6 = ttk.Frame(VVITab)
        row6.pack()
        row7 = ttk.Frame(VVITab)
        row7.pack()
        row8 = ttk.Frame(VVITab)
        row8.pack()
        tk.Label(row1, text="Lower Rate Limit (ppm)").pack(side="left", padx=26, pady=5)
        VVILRL = tk.Scale(row1, from_=50, to=175, length=600, tickinterval=15, orient=tk.HORIZONTAL)
        VVILRL.pack(side="left", padx=5, pady=5)
        tk.Label(row2, text="Upper Rate Limit (ppm)").pack(side="left", padx=26, pady=5)
        VVIURL = tk.Scale(row2, from_=75, to=175, length=600, tickinterval=15, orient=tk.HORIZONTAL)
        VVIURL.pack(side="left", padx=5, pady=5)
        tk.Label(row3, text="Ventrical Amplitude (V)").pack(side="left", padx=27, pady=5)
        VVIVA = tk.Scale(row3, from_=0.5, to=5, resolution=0.5, length=600, tickinterval=0.5, orient=tk.HORIZONTAL)
        VVIVA.pack(side="left", padx=5, pady=5)
        tk.Label(row4, text="Ventricular Pulse Width (ms)").pack(side="left", padx=13, pady=5)
        VVIPW = tk.Scale(row4, from_=1, to=10, length=600, tickinterval=1, orient=tk.HORIZONTAL)
        VVIPW.pack(side="left", padx=5, pady=5)
        tk.Label(row5, text="Ventricular Sense Threshold (V) ").pack(side="left", padx=0, pady=5)
        VVIVS = tk.Scale(row5, from_=0.5, to=3.3, resolution=0.1, length=600, tickinterval=0.3, orient=tk.HORIZONTAL)
        VVIVS.pack(side="left", padx=0, pady=5)
        tk.Label(row6, text="VRP (ms)").pack(side="left", padx=63, pady=5)
        VVIVRP = tk.Scale(row6, from_=150, to=500, length=600, tickinterval=20, orient=tk.HORIZONTAL)
        VVIVRP.pack(side="left", padx=5, pady=5)
        tk.Button(row7, text="Submit", command=lambda:
                  update_info(4, VVILRL.get(), VVIURL.get(), 3, VVIVA.get(), 10, VVIPW.get(), 2.75, VVIVS.get(), 300, VVIVRP.get(), 120, 0, 150, 4, 10, 8, 2, UserID)).pack(side="bottom", pady=5)
        tk.Label(row8, text="User: " + UserID).pack(side="left", padx=0, pady=5)
        tk.Label(row8, text=" ").pack(side="left", padx=180, pady=5)
        tk.Button(row8, text="Atrium Egram", command=lambda:
                  _egramSwitch(1)).pack(side="left", pady=5)
        tk.Button(row8, text="Ventricle Egram", command=lambda:
                  _egramSwitch(2)).pack(side="left", pady=5)
        tk.Button(row8, text="Dual Egram", command=lambda:
                  _egramSwitch(3)).pack(side="left", pady=5)


        # DOO
        row1 = ttk.Frame(DOOTab)
        row1.pack()
        row2 = ttk.Frame(DOOTab)
        row2.pack()
        row3 = ttk.Frame(DOOTab)
        row3.pack()
        row4 = ttk.Frame(DOOTab)
        row4.pack()
        row5 = ttk.Frame(DOOTab)
        row5.pack()
        row6 = ttk.Frame(DOOTab)
        row6.pack()
        row7 = ttk.Frame(DOOTab)
        row7.pack()
        row8 = ttk.Frame(DOOTab)
        row8.pack()
        row9 = ttk.Frame(DOOTab)
        row9.pack()
        tk.Label(row1, text="Lower Rate Limit (ppm)").pack(side="left", padx=20, pady=5)
        DOOLRL = tk.Scale(row1, from_=50, to=175, length=600, tickinterval=15, orient=tk.HORIZONTAL)
        DOOLRL.pack(side="right", padx=5, pady=5)
        tk.Label(row2, text="Upper Rate Limit (ppm)").pack(side="left", padx=20, pady=5)
        DOOURL = tk.Scale(row2, from_=75, to=175, length=600, tickinterval=15, orient=tk.HORIZONTAL)
        DOOURL.pack(side="right", padx=5, pady=5)
        tk.Label(row3, text="Fixed AV Delay (ms)").pack(side="left", padx=30, pady=5)
        DOOFAVD = tk.Scale(row3, from_=70, to=300, length=600, tickinterval=20, orient=tk.HORIZONTAL)
        DOOFAVD.pack(side="left", padx=5, pady=5)
        tk.Label(row4, text="Atrial Amplitude (V)").pack(side="left", padx=30, pady=5)
        DOOAA = tk.Scale(row4, from_=0.5, to=5, resolution=0.5, length=600, tickinterval=0.5, orient=tk.HORIZONTAL)
        DOOAA.pack(side="right", padx=5, pady=5)
        tk.Label(row5, text="Ventricular Amplitude (V)").pack(side="left", padx=15, pady=5)
        DOOVA = tk.Scale(row5, from_=0.5, to=5, resolution=0.5, length=600, tickinterval=0.5, orient=tk.HORIZONTAL)
        DOOVA.pack(side="right", padx=5, pady=5)
        tk.Label(row6, text="Atrial Pulse Width (ms)").pack(side="left", padx=21, pady=5)
        DOOAPW = tk.Scale(row6, from_=1, to=10, length=600, tickinterval=1, orient=tk.HORIZONTAL)
        DOOAPW.pack(side="right", padx=5, pady=5)
        tk.Label(row7, text="Ventricular Pulse Width (ms)").pack(side="left", padx=7, pady=5)
        DOOVPW = tk.Scale(row7, from_=1, to=10, length=600, tickinterval=1, orient=tk.HORIZONTAL)
        DOOVPW.pack(side="right", padx=5, pady=5)
        tk.Button(row8, text="Submit", command=lambda:
                  update_info(5, DOOLRL.get(), DOOURL.get(), DOOAA.get(), DOOVA.get(), DOOAPW.get(), DOOVPW.get(), 2.75, 2.75, 300, 300, 120, 0, DOOFAVD.get(), 4, 10, 8, 2, UserID)).pack(side="bottom", pady=5)
        tk.Label(row9, text="User: " + UserID).pack(side="left", padx=0, pady=5)
        tk.Label(row9, text=" ").pack(side="left", padx=180, pady=5)
        tk.Button(row9, text="Atrium Egram", command=lambda:
                  _egramSwitch(1)).pack(side="left", pady=5)
        tk.Button(row9, text="Ventricle Egram", command=lambda:
                  _egramSwitch(2)).pack(side="left", pady=5)
        tk.Button(row9, text="Dual Egram", command=lambda:
                  _egramSwitch(3)).pack(side="left", pady=5)


        # AOOR
        row1 = ttk.Frame(AOORTab)
        row1.pack()
        row2 = ttk.Frame(AOORTab)
        row2.pack()
        row3 = ttk.Frame(AOORTab)
        row3.pack()
        row4 = ttk.Frame(AOORTab)
        row4.pack()
        row5 = ttk.Frame(AOORTab)
        row5.pack()
        row10 = ttk.Frame(AOORTab)
        row10.pack()
        row11 = ttk.Frame(AOORTab)
        row11.pack()
        tk.Label(row1, text="Lower Rate Limit (ppm)").pack(side="left", padx=6, pady=5)
        AOORLRL = tk.Scale(row1, from_=50, to=175, length=300, tickinterval=15, orient=tk.HORIZONTAL)
        AOORLRL.pack(side="left", padx=5, pady=5)
        tk.Label(row2, text="Upper Rate Limit (ppm)").pack(side="left", padx=5, pady=5)
        AOORURL = tk.Scale(row2, from_=75, to=175, length=300, tickinterval=15, orient=tk.HORIZONTAL)
        AOORURL.pack(side="left", padx=5, pady=5)
        tk.Label(row3, text="Max Sensor Rate (ppm)").pack(side="left", padx=6, pady=5)
        AOORMSR = tk.Scale(row3, from_=50, to=175, length=300, tickinterval=10, orient=tk.HORIZONTAL)
        AOORMSR.pack(side="left", padx=5, pady=5)
        tk.Label(row4, text="Atrial Amplitude (V)").pack(side="left", padx=15, pady=5)
        AOORAA = tk.Scale(row4, from_=0.5, to=5, resolution=0.5, length=300, tickinterval=0.5, orient=tk.HORIZONTAL)
        AOORAA.pack(side="left", padx=5, pady=5)
        tk.Label(row1, text="Atrial Pulse Width (ms)").pack(side="left", padx=12, pady=5)
        AOORAPW = tk.Scale(row1, from_=1, to=10, length=300, tickinterval=1, orient=tk.HORIZONTAL)
        AOORAPW.pack(side="left", padx=5, pady=5)
        tk.Label(row2, text="Reaction Time (s)").pack(side="left", padx=29, pady=5)
        AOORRT = tk.Scale(row2, from_=1, to=30, length=300, tickinterval=2, orient=tk.HORIZONTAL)
        AOORRT.pack(side="left", padx=5, pady=5)
        tk.Label(row3, text="Recovery Time(s)").pack(side="left", padx=28, pady=5)
        AOORRCT = tk.Scale(row3, from_=5, to=30, length=300, tickinterval=2, orient=tk.HORIZONTAL)
        AOORRCT.pack(side="left", padx=5, pady=5)
        tk.Label(row4, text="Response Factor (Slow-Fast)").pack(side="left", padx=0, pady=5)
        AOORRF = tk.Scale(row4, from_=1, to=16, length=300, tickinterval=1, orient=tk.HORIZONTAL)
        AOORRF.pack(side="left", padx=5, pady=5)
        tk.Label(row5, text="Activity Threshold (Low-High)").pack(side="left", padx=36, pady=5)
        AOORAT = tk.Scale(row5, from_=1, to=4, length=300, tickinterval=1, orient=tk.HORIZONTAL)
        AOORAT.pack(side="left", padx=5, pady=5)
        tk.Button(row10, text="Submit", command=lambda:
                  update_info(6, AOORLRL.get(), AOORURL.get(), AOORAA.get(), 3, AOORAPW.get(), 10, 2.75, 2.75, 300, 300, AOORMSR.get(), 0, 150, AOORRT.get(), AOORRCT.get(), AOORRF.get(), AOORAT.get(), UserID)).pack(side="bottom", pady=5)
        tk.Label(row11, text="User: " + UserID).pack(side="left", padx=0, pady=5)
        tk.Label(row11, text=" ").pack(side="left", padx=180, pady=5)
        tk.Button(row11, text="Atrium Egram", command=lambda:
                  _egramSwitch(1)).pack(side="left", pady=5)
        tk.Button(row11, text="Ventricle Egram", command=lambda:
                  _egramSwitch(2)).pack(side="left", pady=5)
        tk.Button(row11, text="Dual Egram", command=lambda:
                  _egramSwitch(3)).pack(side="left", pady=5)


        # VOOR
        row1 = ttk.Frame(VOORTab)
        row1.pack()
        row2 = ttk.Frame(VOORTab)
        row2.pack()
        row3 = ttk.Frame(VOORTab)
        row3.pack()
        row4 = ttk.Frame(VOORTab)
        row4.pack()
        row5 = ttk.Frame(VOORTab)
        row5.pack()
        row10 = ttk.Frame(VOORTab)
        row10.pack()
        row11 = ttk.Frame(VOORTab)
        row11.pack()
        tk.Label(row1, text="Lower Rate Limit (ppm)").pack(side="left", padx=10, pady=5)
        VOORLRL = tk.Scale(row1, from_=50, to=175, length=300, tickinterval=15, orient=tk.HORIZONTAL)
        VOORLRL.pack(side="left", padx=5, pady=5)
        tk.Label(row2, text="Upper Rate Limit (ppm)").pack(side="left", padx=10, pady=5)
        VOORURL = tk.Scale(row2, from_=75, to=175, length=300, tickinterval=15, orient=tk.HORIZONTAL)
        VOORURL.pack(side="left", padx=5, pady=5)
        tk.Label(row3, text="Max Sensor Rate (ppm)").pack(side="left", padx=10, pady=5)
        VOORMSR = tk.Scale(row3, from_=50, to=175, length=300, tickinterval=10, orient=tk.HORIZONTAL)
        VOORMSR.pack(side="left", padx=5, pady=5)
        tk.Label(row4, text="Ventricular Amplitude (V)").pack(side="left", padx=5, pady=5)
        VOORVA = tk.Scale(row4, from_=0.5, to=5, resolution=0.5, length=300, tickinterval=0.5, orient=tk.HORIZONTAL)
        VOORVA.pack(side="left", padx=5, pady=5)
        tk.Label(row1, text="Ventricular Pulse Width (ms)").pack(side="left", padx=5, pady=5)
        VOORVPW = tk.Scale(row1, from_=1, to=10, length=300, tickinterval=1, orient=tk.HORIZONTAL)
        VOORVPW.pack(side="left", padx=5, pady=5)
        tk.Label(row2, text="Reaction Time (s)").pack(side="left", padx=34, pady=5)
        VOORRT = tk.Scale(row2, from_=1, to=30, length=300, tickinterval=2, orient=tk.HORIZONTAL)
        VOORRT.pack(side="left", padx=5, pady=5)
        tk.Label(row3, text="Recovery Time(s)").pack(side="left", padx=35, pady=5)
        VOORRCT = tk.Scale(row3, from_=5, to=30, length=300, tickinterval=2, orient=tk.HORIZONTAL)
        VOORRCT.pack(side="left", padx=5, pady=5)
        tk.Label(row4, text="Response Factor (Slow-Fast)").pack(side="left", padx=5, pady=5)
        VOORRF = tk.Scale(row4, from_=1, to=16, length=300, tickinterval=1, orient=tk.HORIZONTAL)
        VOORRF.pack(side="left", padx=5, pady=5)
        tk.Label(row5, text="Activity Threshold (Low-High)").pack(side="left", padx=36, pady=5)
        VOORAT = tk.Scale(row5, from_=1, to=4, length=300, tickinterval=1, orient=tk.HORIZONTAL)
        VOORAT.pack(side="left", padx=5, pady=5)
        tk.Button(row10, text="Submit", command=lambda:
                  update_info(7, VOORLRL.get(), VOORURL.get(), 3, VOORVA.get(), 10, VOORVPW.get(), 2.75, 2.75, 300, 300, VOORMSR.get(), 0, 150, VOORRT.get(), VOORRCT.get(), VOORRF.get(), VOORAT.get(), UserID)).pack(side="bottom", pady=5)
        tk.Label(row11, text="User: " + UserID).pack(side="left", padx=0, pady=5)
        tk.Label(row11, text=" ").pack(side="left", padx=180, pady=5)
        tk.Button(row11, text="Atrium Egram", command=lambda:
                  _egramSwitch(1)).pack(side="left", pady=5)
        tk.Button(row11, text="Ventricle Egram", command=lambda:
                  _egramSwitch(2)).pack(side="left", pady=5)
        tk.Button(row11, text="Dual Egram", command=lambda:
                  _egramSwitch(3)).pack(side="left", pady=5)


        # AAIR
        row1 = ttk.Frame(AAIRTab)
        row1.pack()
        row2 = ttk.Frame(AAIRTab)
        row2.pack()
        row3 = ttk.Frame(AAIRTab)
        row3.pack()
        row4 = ttk.Frame(AAIRTab)
        row4.pack()
        row5 = ttk.Frame(AAIRTab)
        row5.pack()
        row6 = ttk.Frame(AAIRTab)
        row6.pack()
        row7 = ttk.Frame(AAIRTab)
        row7.pack()
        row8 = ttk.Frame(AAIRTab)
        row8.pack()
        row9 = ttk.Frame(AAIRTab)
        row9.pack()
        row10 = ttk.Frame(AAIRTab)
        row10.pack()
        row11 = ttk.Frame(AAIRTab)
        row11.pack()
        row12 = ttk.Frame(AAIRTab)
        row12.pack()
        row13 = ttk.Frame(AAIRTab)
        row13.pack()
        row14 = ttk.Frame(AAIRTab)
        row14.pack()
        tk.Label(row1, text="Lower Rate Limit (ppm)").pack(side="left", padx=9, pady=5)
        AAIRLRL = tk.Scale(row1, from_=50, to=175, length=300, tickinterval=15, orient=tk.HORIZONTAL)
        AAIRLRL.pack(side="left", padx=2, pady=5)
        tk.Label(row2, text="Upper Rate Limit (ppm)").pack(side="left", padx=9, pady=5)
        AAIRURL = tk.Scale(row2, from_=75, to=175, length=300, tickinterval=15, orient=tk.HORIZONTAL)
        AAIRURL.pack(side="left", padx=2, pady=5)
        tk.Label(row3, text="Max Sensor Rate (ppm)").pack(side="left", padx=9, pady=5)
        AAIRMSR = tk.Scale(row3, from_=50, to=175, length=300, tickinterval=10, orient=tk.HORIZONTAL)
        AAIRMSR.pack(side="left", padx=2, pady=5)
        tk.Label(row4, text="Atrial Amplitude (V)").pack(side="left", padx=19, pady=5)
        AAIRAA = tk.Scale(row4, from_=0.5, resolution=0.5, to=5, length=300, tickinterval=0.5, orient=tk.HORIZONTAL)
        AAIRAA.pack(side="left", padx=2, pady=5)
        tk.Label(row5, text="Atrial Pulse Width (ms)").pack(side="left", padx=12, pady=5)
        AAIRAPW = tk.Scale(row5, from_=1, to=10, length=300, tickinterval=1, orient=tk.HORIZONTAL)
        AAIRAPW.pack(side="left", padx=0, pady=5)
        tk.Label(row6, text="Atrial Sense Threshold (V) ").pack(side="left", padx=0, pady=5)
        AAIRAS = tk.Scale(row6, from_=0.5, to=3.3, resolution=0.1, length=300, tickinterval=0.3, orient=tk.HORIZONTAL)
        AAIRAS.pack(side="left", padx=0, pady=5)
        tk.Label(row1, text="ARP (ms)").pack(side="left", padx=55, pady=5)
        AAIRARP = tk.Scale(row1, from_=150, to=500, length=300, tickinterval=30, orient=tk.HORIZONTAL)
        AAIRARP.pack(side="left", padx=5, pady=5)
        tk.Label(row2, text="PVARP (ms)").pack(side="left", padx=48, pady=5)#########################################
        AAIRPVARP = tk.Scale(row2, from_=150, to=500, length=300, tickinterval=30, orient=tk.HORIZONTAL)
        AAIRPVARP.pack(side="left", padx=5, pady=5)
        tk.Label(row3, text="Reaction Time (s)").pack(side="left", padx=33, pady=5)
        AAIRRT = tk.Scale(row3, from_=1, to=30, length=300, tickinterval=2, orient=tk.HORIZONTAL)
        AAIRRT.pack(side="left", padx=5, pady=5)
        tk.Label(row4, text="Recovery Time(s)").pack(side="left", padx=34, pady=5)
        AAIRRCT = tk.Scale(row4, from_=5, to=30, length=300, tickinterval=2, orient=tk.HORIZONTAL)
        AAIRRCT.pack(side="left", padx=5, pady=5)
        tk.Label(row5, text="Response Factor (Slow-Fast)").pack(side="left", padx=7, pady=5)
        AAIRRF = tk.Scale(row5, from_=1, to=16, length=300, tickinterval=1, orient=tk.HORIZONTAL)
        AAIRRF.pack(side="left", padx=1, pady=5)
        tk.Label(row6, text="Activity Threshold (Low-High)").pack(side="left", padx=2, pady=5)
        AAIRAT = tk.Scale(row6, from_=1, to=4, length=300, tickinterval=1, orient=tk.HORIZONTAL)
        AAIRAT.pack(side="left", padx=0, pady=5)
        tk.Button(row13, text="Submit", command=lambda:       
                  update_info(8, AAIRLRL.get(), AAIRURL.get(), AAIRAA.get(), 3, AAIRAPW.get(), 10, AAIRAS.get(), 2.75, AAIRARP.get(), 300, AAIRMSR.get(), 0, 150, AAIRRT.get(), AAIRRCT.get(), AAIRRF.get(), AAIRAT.get(), UserID)).pack(side="bottom", pady=5)
        tk.Label(row14, text="User: " + UserID).pack(side="left", padx=0, pady=5)
        tk.Label(row14, text=" ").pack(side="left", padx=180, pady=5)
        tk.Button(row14, text="Atrium Egram", command=lambda:
                  _egramSwitch(1)).pack(side="left", pady=5)
        tk.Button(row14, text="Ventricle Egram", command=lambda:
                  _egramSwitch(2)).pack(side="left", pady=5)
        tk.Button(row14, text="Dual Egram", command=lambda:
                  _egramSwitch(3)).pack(side="left", pady=5)


        # VVIR
        row1 = ttk.Frame(VVIRTab)
        row1.pack()
        row2 = ttk.Frame(VVIRTab)
        row2.pack()
        row3 = ttk.Frame(VVIRTab)
        row3.pack()
        row4 = ttk.Frame(VVIRTab)
        row4.pack()
        row5 = ttk.Frame(VVIRTab)
        row5.pack()
        row6 = ttk.Frame(VVIRTab)
        row6.pack()
        row7 = ttk.Frame(VVIRTab)
        row7.pack()
        row8 = ttk.Frame(VVIRTab)
        row8.pack()
        row9 = ttk.Frame(VVIRTab)
        row9.pack()
        row10 = ttk.Frame(VVIRTab)
        row10.pack()
        row11 = ttk.Frame(VVIRTab)
        row11.pack()
        row12 = ttk.Frame(VVIRTab)
        row12.pack()
        row13 = ttk.Frame(VVIRTab)
        row13.pack()
        tk.Label(row1, text="Lower Rate Limit (ppm)").pack(side="left", padx=17, pady=5)
        VVIRLRL = tk.Scale(row1, from_=50, to=175, length=300, tickinterval=15, orient=tk.HORIZONTAL)
        VVIRLRL.pack(side="left", padx=5, pady=5)
        tk.Label(row2, text="Upper Rate Limit (ppm)").pack(side="left", padx=17, pady=5)
        VVIRURL = tk.Scale(row2, from_=75, to=175, length=300, tickinterval=15, orient=tk.HORIZONTAL)
        VVIRURL.pack(side="left", padx=5, pady=5)
        tk.Label(row3, text="Max Sensor Rate (ppm)").pack(side="left", padx=17, pady=5)
        VVIRMSR = tk.Scale(row3, from_=50, to=175, length=300, tickinterval=10, orient=tk.HORIZONTAL)
        VVIRMSR.pack(side="left", padx=5, pady=5)
        tk.Label(row4, text="Ventricular Amplitude (V)").pack(side="left", padx=12, pady=5)
        VVIRVA = tk.Scale(row4, from_=0.5, to=5, resolution=0.5, length=300, tickinterval=0.5, orient=tk.HORIZONTAL)
        VVIRVA.pack(side="left", padx=5, pady=5)
        tk.Label(row5, text="Ventricular Pulse Width (ms)").pack(side="left", padx=5, pady=5)
        VVIRVPW = tk.Scale(row5, from_=1, to=10, length=300, tickinterval=1, orient=tk.HORIZONTAL)
        VVIRVPW.pack(side="left", padx=5, pady=5)
        tk.Label(row1, text="Ventricular Sense Threshold (V) ").pack(side="left", padx=0, pady=5)
        VVIRVS = tk.Scale(row1, from_=0.5, to=3.3, resolution=0.1, length=300, tickinterval=0.3, orient=tk.HORIZONTAL)
        VVIRVS.pack(side="left", padx=0, pady=5)
        tk.Label(row2, text="VRP (ms)").pack(side="left", padx=63, pady=5)
        VVIRVRP = tk.Scale(row2, from_=150, to=500, length=300, tickinterval=30, orient=tk.HORIZONTAL)
        VVIRVRP.pack(side="left", padx=1, pady=5)
        tk.Label(row3, text="Reaction Time (s)").pack(side="left", padx=40, pady=5)
        VVIRRT = tk.Scale(row3, from_=2, to=30, length=300, tickinterval=2, orient=tk.HORIZONTAL)
        VVIRRT.pack(side="left", padx=1, pady=5)
        tk.Label(row4, text="Recovery Time(s)").pack(side="left", padx=41, pady=5)
        VVIRRCT = tk.Scale(row4, from_=5, to=30, length=300, tickinterval=2, orient=tk.HORIZONTAL)
        VVIRRCT.pack(side="left", padx=1, pady=5)
        tk.Label(row5, text="Response Factor (Slow-Fast)").pack(side="left", padx=12, pady=5)
        VVIRRF = tk.Scale(row5, from_=1, to=16, length=300, tickinterval=1, orient=tk.HORIZONTAL)
        VVIRRF.pack(side="left", padx=1, pady=5)
        tk.Label(row11, text="Activity Threshold (Low-High)").pack(side="left", padx=33, pady=5)
        VVIRAT = tk.Scale(row11, from_=1, to=4, length=300, tickinterval=1, orient=tk.HORIZONTAL)
        VVIRAT.pack(side="left", padx=5, pady=5)
        tk.Button(row12, text="Submit", command=lambda:
                  update_info(9, VVIRLRL.get(), VVIRURL.get(), 3, VVIRVA.get(), 10, VVIRVPW.get(), 2.75, VVIRVS.get(), 300, VVIRVRP.get(), VVIRMSR.get(), 0, 150, VVIRRT.get(), VVIRRCT.get(), VVIRRF.get(), VVIRAT.get(), UserID)).pack(side="bottom", pady=5)
        tk.Label(row13, text="User: " + UserID).pack(side="left", padx=0, pady=5)
        tk.Label(row13, text=" ").pack(side="left", padx=180, pady=5)
        tk.Button(row13, text="Atrium Egram", command=lambda:
                  _egramSwitch(1)).pack(side="left", pady=5)
        tk.Button(row13, text="Ventricle Egram", command=lambda:
                  _egramSwitch(2)).pack(side="left", pady=5)
        tk.Button(row13, text="Dual Egram", command=lambda:
                  _egramSwitch(3)).pack(side="left", pady=5)


        # DOOR
        row1 = ttk.Frame(DOORTab)
        row1.pack()
        row2 = ttk.Frame(DOORTab)
        row2.pack()
        row3 = ttk.Frame(DOORTab)
        row3.pack()
        row4 = ttk.Frame(DOORTab)
        row4.pack()
        row5 = ttk.Frame(DOORTab)
        row5.pack()
        row6 = ttk.Frame(DOORTab)
        row6.pack()
        row7 = ttk.Frame(DOORTab)
        row7.pack()
        row8 = ttk.Frame(DOORTab)
        row8.pack()
        row9 = ttk.Frame(DOORTab)
        row9.pack()
        row10 = ttk.Frame(DOORTab)
        row10.pack()
        row11 = ttk.Frame(DOORTab)
        row11.pack()
        row12 = ttk.Frame(DOORTab)
        row12.pack()
        row13 = ttk.Frame(DOORTab)
        row13.pack()
        row14 = ttk.Frame(DOORTab)
        row14.pack()
        tk.Label(row1, text="Lower Rate Limit (ppm)").pack(side="left", padx=10, pady=5)
        DOORLRL = tk.Scale(row1, from_=50, to=175, length=300, tickinterval=15, orient=tk.HORIZONTAL)
        DOORLRL.pack(side="left", padx=5, pady=5)
        tk.Label(row2, text="Upper Rate Limit (ppm)").pack(side="left", padx=10, pady=5)
        DOORURL = tk.Scale(row2, from_=75, to=175, length=300, tickinterval=15, orient=tk.HORIZONTAL)
        DOORURL.pack(side="left", padx=5, pady=5)
        tk.Label(row3, text="Max Sensor Rate (ppm)").pack(side="left", padx=10, pady=5)
        DOORMSR = tk.Scale(row3, from_=50, to=175, length=300, tickinterval=10, orient=tk.HORIZONTAL)
        DOORMSR.pack(side="left", padx=5, pady=5)
        tk.Label(row4, text="Fixed AV Delay (ms)").pack(side="left", padx=18, pady=5)
        DOORFAVD = tk.Scale(row4, from_=70, to=300, length=300, tickinterval=20, orient=tk.HORIZONTAL)
        DOORFAVD.pack(side="left", padx=5, pady=5)
        tk.Label(row5, text="Atrial Amplitude (V)").pack(side="left", padx=19, pady=5)
        DOORAA = tk.Scale(row5, from_=0.5, to=5, resolution=0.5, length=300, tickinterval=0.5, orient=tk.HORIZONTAL)
        DOORAA.pack(side="left", padx=5, pady=5)
        tk.Label(row6, text="Ventricular Amplitude (V)").pack(side="left", padx=5, pady=5)
        DOORVA = tk.Scale(row6, from_=0.5, to=5, resolution=0.5, length=300, tickinterval=0.5, orient=tk.HORIZONTAL)
        DOORVA.pack(side="left", padx=5, pady=5)
        tk.Label(row1, text="Atrial Pulse Width (ms)").pack(side="left", padx=20, pady=5)
        DOORAPW = tk.Scale(row1, from_=1, to=10, length=300, tickinterval=1, orient=tk.HORIZONTAL)
        DOORAPW.pack(side="left", padx=5, pady=5)
        tk.Label(row2, text="Ventricular Pulse Width (ms)").pack(side="left", padx=5, pady=5)
        DOORVPW = tk.Scale(row2, from_=1, to=10, length=300, tickinterval=1, orient=tk.HORIZONTAL)
        DOORVPW.pack(side="left", padx=5, pady=5)
        tk.Label(row3, text="Reaction Time (s)").pack(side="left", padx=34, pady=5)
        DOORRT = tk.Scale(row3, from_=1, to=30, length=300, tickinterval=2, orient=tk.HORIZONTAL)
        DOORRT.pack(side="left", padx=5, pady=5)
        tk.Label(row4, text="Recovery Time(s)").pack(side="left", padx=35, pady=5)
        DOORRCT = tk.Scale(row4, from_=5, to=30, length=300, tickinterval=2, orient=tk.HORIZONTAL)
        DOORRCT.pack(side="left", padx=5, pady=5)
        tk.Label(row5, text="Response Factor (Slow-Fast)").pack(side="left", padx=5, pady=5)
        DOORRF = tk.Scale(row5, from_=1, to=16, length=300, tickinterval=1, orient=tk.HORIZONTAL)
        DOORRF.pack(side="left", padx=5, pady=5)
        tk.Label(row6, text="Activity Threshold (Low-High)").pack(side="left", padx=0, pady=5)
        DOORAT = tk.Scale(row6, from_=1, to=4, length=300, tickinterval=1, orient=tk.HORIZONTAL)
        DOORAT.pack(side="left", padx=5, pady=5)
        tk.Button(row13, text="Submit", command=lambda:
                  update_info(10, DOORLRL.get(), DOORURL.get(), DOORAA.get(), DOORVA.get(), DOORAPW.get(), DOORVPW.get(), 2.75, 2.75, 300, 300, DOORMSR.get(), 150, DOORFAVD.get(), DOORRT.get(), DOORRCT.get(), DOORRF.get(), DOORAT.get(), UserID)).pack(side="bottom", pady=5)
        tk.Label(row14, text="User: " + UserID).pack(side="left", padx=0, pady=5)
        tk.Label(row14, text=" ").pack(side="left", padx=180, pady=5)
        tk.Button(row14, text="Atrium Egram", command=lambda:
                  _egramSwitch(1)).pack(side="left", pady=5)
        tk.Button(row14, text="Ventricle Egram", command=lambda:
                  _egramSwitch(2)).pack(side="left", pady=5)
        tk.Button(row14, text="Dual Egram", command=lambda:
                  _egramSwitch(3)).pack(side="left", pady=5)

        
        # DDDR
        """ Pacemaker not programmed to function in DDDR mode yet, but DCM has functioning DDDR tab for when it is """
        row1 = ttk.Frame(DDDRTab)
        row1.pack()
        row2 = ttk.Frame(DDDRTab)
        row2.pack()
        row3 = ttk.Frame(DDDRTab)
        row3.pack()
        row4 = ttk.Frame(DDDRTab)
        row4.pack()
        row5 = ttk.Frame(DDDRTab)
        row5.pack()
        row6 = ttk.Frame(DDDRTab)
        row6.pack()
        row7 = ttk.Frame(DDDRTab)
        row7.pack()
        row8 = ttk.Frame(DDDRTab)
        row8.pack()
        row9 = ttk.Frame(DDDRTab)
        row9.pack()
        row10 = ttk.Frame(DDDRTab)
        row10.pack()
        row11 = ttk.Frame(DDDRTab)
        row11.pack()
        row12 = ttk.Frame(DDDRTab)
        row12.pack()
        row13 = ttk.Frame(DDDRTab)
        row13.pack()
        row14 = ttk.Frame(DDDRTab)
        row14.pack()
        row15 = ttk.Frame(DDDRTab)
        row15.pack()
        row16 = ttk.Frame(DDDRTab)
        row16.pack()
        row17 = ttk.Frame(DDDRTab)
        row17.pack()
        row18 = ttk.Frame(DDDRTab)
        row18.pack()
        row19 = ttk.Frame(DDDRTab)
        row19.pack()
        tk.Label(row1, text="Lower Rate Limit (ppm)").pack(side="left", padx=17, pady=5)
        DDDRLRL = tk.Scale(row1, from_=50, to=175, length=300, tickinterval=15, orient=tk.HORIZONTAL)
        DDDRLRL.pack(side="left", padx=5, pady=0)
        tk.Label(row2, text="Upper Rate Limit (ppm)").pack(side="left", padx=15, pady=5)
        DDDRURL = tk.Scale(row2, from_=75, to=175, length=300, tickinterval=15, orient=tk.HORIZONTAL)
        DDDRURL.pack(side="left", padx=5, pady=0)
        tk.Label(row3, text="Max Sensor Rate (ppm)").pack(side="left", padx=20, pady=5)
        DDDRMSR = tk.Scale(row3, from_=50, to=175, length=300, tickinterval=10, orient=tk.HORIZONTAL)
        DDDRMSR.pack(side="left", padx=2, pady=0)
        tk.Label(row4, text="Fixed AV Delay (ms)").pack(side="left", padx=27, pady=5)
        DDDRFAVD = tk.Scale(row4, from_=70, to=300, length=300, tickinterval=20, orient=tk.HORIZONTAL)
        DDDRFAVD.pack(side="left", padx=1, pady=0)
        tk.Label(row5, text="Atrial Amplitude (V)").pack(side="left", padx=27, pady=5)
        DDDRAA = tk.Scale(row5, from_=0.5, to=5, resolution=0.5, length=300, tickinterval=0.5, orient=tk.HORIZONTAL)
        DDDRAA.pack(side="left", padx=5, pady=0)
        tk.Label(row6, text="Ventricular Amplitude (V)").pack(side="left", padx=12, pady=5)
        DDDRVA = tk.Scale(row6, from_=0.5, to=5, resolution=0.5, length=300, tickinterval=0.5, orient=tk.HORIZONTAL)
        DDDRVA.pack(side="left", padx=5, pady=0)
        tk.Label(row7, text="Atrial Pulse Width (ms)").pack(side="left", padx=18, pady=5)
        DDDRAPW = tk.Scale(row7, from_=1, to=10, length=300, tickinterval=1, orient=tk.HORIZONTAL)
        DDDRAPW.pack(side="left", padx=5, pady=0)
        tk.Label(row8, text="Ventricular Pulse Width (ms)").pack(side="left", padx=6, pady=5)
        DDDRVPW = tk.Scale(row8, from_=1, to=10, length=300, tickinterval=1, orient=tk.HORIZONTAL)
        DDDRVPW.pack(side="left", padx=0, pady=0)
        tk.Label(row1, text="Atrial Sense Threshold (V) ").pack(side="left", padx=16, pady=5)
        DDDRAS = tk.Scale(row1, from_=0.5, to=3.3, resolution=0.1, length=300, tickinterval=0.3, orient=tk.HORIZONTAL)
        DDDRAS.pack(side="left", padx=6, pady=0)
        tk.Label(row2, text="Ventricular Sense Threshold (V) ").pack(side="left", padx=5, pady=5)
        DDDRVS = tk.Scale(row2, from_=0.5, to=3.3, resolution=0.1, length=300, tickinterval=0.3, orient=tk.HORIZONTAL)
        DDDRVS.pack(side="left", padx=0, pady=0)
        tk.Label(row3, text="ARP (ms)").pack(side="left", padx=67, pady=5)
        DDDRARP = tk.Scale(row3, from_=150, to=500, length=300, tickinterval=30, orient=tk.HORIZONTAL)
        DDDRARP.pack(side="left", padx=5, pady=5)
        tk.Label(row4, text="VRP (ms)").pack(side="left", padx=70, pady=5)
        DDDRVRP = tk.Scale(row4, from_=150, to=500, length=300, tickinterval=30, orient=tk.HORIZONTAL)
        DDDRVRP.pack(side="left", padx=0, pady=5)
        tk.Label(row5, text="PVARP (ms)").pack(side="left", padx=57, pady=5)
        DDDRPVARP = tk.Scale(row5, from_=150, to=500, length=300, tickinterval=30, orient=tk.HORIZONTAL)
        DDDRPVARP.pack(side="left", padx=5, pady=5)
        tk.Label(row6, text="Reaction Time (s)").pack(side="left", padx=42, pady=5)
        DDDRRT = tk.Scale(row6, from_=1, to=30, length=300, tickinterval=2, orient=tk.HORIZONTAL)
        DDDRRT.pack(side="left", padx=5, pady=0)
        tk.Label(row7, text="Recovery Time(s)").pack(side="left", padx=43, pady=5)
        DDDRRCT = tk.Scale(row7, from_=5, to=30, length=300, tickinterval=2, orient=tk.HORIZONTAL)
        DDDRRCT.pack(side="left", padx=5, pady=0)
        tk.Label(row8, text="Response Factor (Slow-Fast)").pack(side="left", padx=17, pady=5)
        DDDRRF = tk.Scale(row8, from_=1, to=16, length=300, tickinterval=1, orient=tk.HORIZONTAL)
        DDDRRF.pack(side="left", padx=7, pady=0)
        tk.Label(row17, text="Activity Threshold (Low-High)").pack(side="left", padx=8, pady=5)
        DDDRAT = tk.Scale(row17, from_=1, to=4, length=300, tickinterval=1, orient=tk.HORIZONTAL)
        DDDRAT.pack(side="left", padx=5, pady=0)
        tk.Button(row18, text="Submit", command=lambda:
                  update_info(11, DDDRLRL.get(), DDDRURL.get(), DDDRAA.get(), DDDRVA.get(), DDDRAPW.get(), DDDRVPW.get(), DDDRAS.get(), DDDRVS.get(), DDDRARP.get(), DDDRVRP.get(), DDDRMSR.get(), DDDRPVARP.get(), DDDRFAVD.get(), DDDRRT.get(), DDDRRCT.get(), DDDRRF.get(), DDDRAT.get(), UserID)).pack(side="bottom", pady=5)
        tk.Label(row19, text="User: " + UserID).pack(side="left", padx=0, pady=5)
        tk.Label(row19, text=" ").pack(side="left", padx=180, pady=5)
        tk.Button(row19, text="Atrium Egram", command=lambda:
                  _egramSwitch(1)).pack(side="left", pady=5)
        tk.Button(row19, text="Ventricle Egram", command=lambda:
                  _egramSwitch(2)).pack(side="left", pady=5)
        tk.Button(row19, text="Dual Egram", command=lambda:
                  _egramSwitch(3)).pack(side="left", pady=5)
