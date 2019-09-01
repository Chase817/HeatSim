#!/usr/bin/env python3

#
# Written by Chase Hill 2017
#

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import animation
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import ttk

###############################################################################
# GUI class
###############################################################################
class GUI(object):
    def __init__(self,root):
        self.root = root
        
        #######################################################################
        
        # Create menu bar
        self.menu_bar = tk.Menu(root)

        # Create submenus
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.about_menu = tk.Menu(self.menu_bar, tearoff=0)

        # Add commands to submenus
        self.file_menu.add_command(label="Quit HeatSim", command=quit)
        self.about_menu.add_command(label="What is HeatSim?",
                                    command=self.popup)

        # Add drop down submenus to UI
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.menu_bar.add_cascade(label="About", menu=self.about_menu)

        root.config(menu=self.menu_bar)
        
        #######################################################################
        
        # Window title
        root.title("HeatSim")
        
        #######################################################################
        
        # Window size
        root.geometry("1100x500+460+140")
        
        #######################################################################
        
        self.r = 0  # Used to conviniently increment the row number of a widget
        
        # sticky option makes the widget align itself to cardinal directions
        tk.Label(root,text="Timespan (frames):").grid(row=self.r,column=0,
                                                      columnspan=2,sticky=tk.W)

        self.nt = tk.Entry(root,width=3)
        self.nt.insert(0, '100')
        self.nt.grid(row=self.r, column=2)
        
        #####        
        
        self.r += 1
        
        tk.Label(root,text="Plate size (x,y): ").grid(row=self.r,column=0,
                                                      columnspan=2,sticky=tk.W)

        self.Lx = tk.Entry(root,width=2)
        self.Lx.insert(0, '5')
        self.Lx.grid(row=self.r, column=2)

        tk.Label(root,text="x").grid(row=self.r, column=3)

        self.Ly = tk.Entry(root,width=2)
        self.Ly.insert(0, '5')
        self.Ly.grid(row=self.r, column=4)

        #####
        
        self.r += 1

        tk.Label(root,text="Alpha (thermal diffusivity): ").grid(row=self.r,
                                             column=0,columnspan=2,sticky=tk.W)

        self.a = tk.Entry(root,width=3)
        self.a.insert(0, '0.5')
        self.a.grid(row=self.r, column=2)

        #####
        
        self.r += 2
        
        tk.Label(root,text="Initial conditions:").grid(row=self.r,column=0,
                                                      columnspan=2,sticky=tk.W)
        
        #####        
        
        self.r += 1

        self.uniformity = tk.IntVar(root)

        # Radio buttons force the user to select one (and only one) option
        tk.Radiobutton(root, variable=self.uniformity,value=1).grid(row=self.r,
                                                                    column=0)
        
        tk.Label(root,text="Uniform initial temperature:").grid(row=self.r,
                                                          column=1,sticky=tk.W)

        self.uniform_temp = tk.Entry(root,width=3)
        self.uniform_temp.insert(0, '50')
        self.uniform_temp.grid(row=self.r, column=2)

        #####
        
        self.r += 1

        tk.Radiobutton(root, variable=self.uniformity,value=0).grid(row=self.r,
                                                                    column=0)
        
        tk.Label(root,text="Initial temperature preset:").grid(row=self.r,
                                                          column=1,sticky=tk.W)

        self.preset = tk.StringVar(root)
 
        self.choices = {'1. T(x,y)=sin(x)','2. T(x,y)=x*y','3. Hot pyramid',
                        '4. Hot circle'}
        self.preset.set('1. T(x,y)=sin(x)') # Set the default option
 
        self.popupMenu = tk.OptionMenu(root, self.preset,*sorted(self.choices))
        self.popupMenu.grid(row=self.r, column=2,columnspan=9,sticky=tk.W)

        #####
        
        self.r += 1

        self.custom_region = tk.IntVar()

        tk.Checkbutton(root, variable=self.custom_region).grid(row=self.r,
                                                               column=0)
        
        # This region select UI could probably be improved to be more consise
        tk.Label(root,text="Initial region temperature: T(").grid(row=self.r,
                                                          column=1,sticky=tk.W)

        self.x1 = tk.Entry(root,width=2)
        self.x1.grid(row=self.r, column=2)

        tk.Label(root,text=":").grid(row=self.r, column=3)

        self.x2 = tk.Entry(root,width=2)
        self.x2.grid(row=self.r, column=4)

        tk.Label(root,text=",").grid(row=self.r, column=5)

        self.y1 = tk.Entry(root,width=2)
        self.y1.grid(row=self.r, column=6)

        tk.Label(root,text=":").grid(row=self.r, column=7)

        self.y2 = tk.Entry(root,width=2)
        self.y2.grid(row=self.r, column=8)

        tk.Label(root,text=")=").grid(row=self.r, column=9)

        self.region_temp = tk.Entry(root,width=3)
        self.region_temp.grid(row=self.r, column=10)

        tk.Label(root,text="   ").grid(row=self.r, column=11)

        #####
        
        self.r += 2

        tk.Label(root,text="Boundary conditions (insulated by default):").grid(
                                 row=self.r, column=0,columnspan=7,sticky=tk.W)
        #####
        
        self.r += 1
        
        self.lDir = tk.IntVar()
        tk.Checkbutton(root, variable=self.lDir).grid(row=self.r,column=0)
        tk.Label(root,text="Left temperature:").grid(row=self.r, column=1,
                                                     sticky=tk.W)
        self.lTemp = tk.Entry(root,width=3)
        self.lTemp.grid(row=self.r, column=2,sticky=tk.W)

        self.r += 1
        self.rDir = tk.IntVar()
        tk.Checkbutton(root, variable=self.rDir).grid(row=self.r,column=0)
        tk.Label(root,text="Right temperature:").grid(row=self.r, column=1,
                                                      sticky=tk.W)
        self.rTemp = tk.Entry(root,width=3)
        self.rTemp.grid(row=self.r, column=2,sticky=tk.W)

        self.r += 1
        self.bDir = tk.IntVar()
        tk.Checkbutton(root, variable=self.bDir).grid(row=self.r,column=0)
        tk.Label(root,text="Bottom temperature:").grid(row=self.r, column=1,
                                                       sticky=tk.W)
        self.bTemp = tk.Entry(root,width=3)
        self.bTemp.grid(row=self.r, column=2,sticky=tk.W)

        self.r += 1
        self.tDir = tk.IntVar()
        tk.Checkbutton(root, variable=self.tDir).grid(row=self.r,column=0)
        tk.Label(root,text="Top temperature:").grid(row=self.r, column=1,
                                                    sticky=tk.W)
        self.tTemp = tk.Entry(root,width=3)
        self.tTemp.grid(row=self.r, column=2,sticky=tk.W)
        
        #####
        
        self.r += 1

        self.print_button = tk.Button(root, text='Run Simulation',
                                      command=self.run)
        
        self.print_button.grid(row=self.r,column=1,columnspan=2)

        #####

        self.r += 2
        
        # Initialize a blank graph to keep all the elements in place and to
        # make the UI more static
        fig = plt.figure()
        fig.add_subplot(111)
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.show()
        canvas.get_tk_widget().grid(row=0,column=12,rowspan=self.r,
                                    sticky=tk.E+tk.N+tk.S)
                                    
    ###########################################################################
    def popup(self):
        top = tk.Toplevel()
        top.title("What is HeatSim?")
        
        about_message = "HeatSim is a 2D heat equation solver/visualizer that"\
                        +" simulates the flow of heat through a plate with "  \
                        +"the given conditions.\n\nHeatSim solves the heat "  \
                        +"equation using the finite-distance numerical method"\
                        +", and supports both Dirichlet and Neumann boundary "\
                        +"conditions.\n\nWritten in Python 3, HeatSim was an "\
                        +"exercise in GUI development and object-oriented "   \
                        +"programming. Lots of time was spent finding a "     \
                        +"consise and powerful design that allows the user "  \
                        +"maximum control without unnecessary pages and UI "  \
                        +"elements. In addition, countless hours went into "  \
                        +"rewriting code to keep the program as stable and "  \
                        +"functional as possible.\n\nChase Hill - 2017"
        
        tk.Message(top, text=about_message, padx=10, pady=10).grid()
        
        dismiss_button = tk.Button(top, text="Dismiss", command=top.destroy)
        dismiss_button.grid()

    ###########################################################################
    def run(self):
        simulation = HeatSim(self)
        simulation.compute(self)
        simulation.animate(self)

###############################################################################
# Simulator class
###############################################################################
class HeatSim(GUI):
    def __init__(self,gui):
        self.nt = int(gui.nt.get())    # Number of time steps (frames)
        self.Lx = float(gui.Lx.get())    # Plate length in x
        self.Ly = float(gui.Ly.get())    # Plate length in y
        self.a = float(gui.a.get())    # Alpha value (thermal diffusivity)
        
        # Retrieve the boolean values for desired modes from the GUI
        self.uniformity = int(gui.uniformity.get())
        self.custom_region = int(gui.custom_region.get())
        self.lDir = int(gui.lDir.get())
        self.rDir = int(gui.rDir.get())
        self.bDir = int(gui.bDir.get())
        self.tDir = int(gui.tDir.get())
        
        # Depending on which modes were selected, retrieve values for each
        if self.uniformity:
            self.uniform_temp = float(gui.uniform_temp.get())
        else:
            self.preset = int(gui.preset.get()[0])-1
        
        if self.custom_region:
            self.region = (float(gui.x1.get()),float(gui.x2.get()),
                           float(gui.y1.get()),float(gui.y2.get()))
            self.region_temp = float(gui.region_temp.get())
        
        if self.lDir:
            self.lTemp = float(gui.lTemp.get())
        if self.rDir:
            self.rTemp = float(gui.rTemp.get())
        if self.bDir:
            self.bTemp = float(gui.bTemp.get())
        if self.tDir:
            self.tTemp = float(gui.tTemp.get())
        
        self.h = 0.1    # dx & dy size, not user selectable because I figured
                        # it would be redundant with plate size options
        
        self.dt = self.h**2 / (8 * self.a) # Found an algorithm for selecting
                                           # this value online and modified it
                                           # via trial and error for stability
        
        self.nx = int(self.Lx/self.h)
        self.ny = int(self.Ly/self.h)
        
        self.k = 0 # Time index for temperature array, initialized

    ###########################################################################
    def compute(self,gui):
        nx = self.nx
        ny = self.ny
        nt = self.nt
        uniformity = self.uniformity
        h = self.h
        custom_region = self.custom_region
        a = self.a
        dt = self.dt
        
        def initPlate(self):
            if uniformity:    # Uniform temperature
                self.T = np.full((nx+2,ny+2,nt),self.uniform_temp,
                                 dtype='float64')
            else:
                self.T = np.zeros((nx+2,ny+2,nt),dtype='float64')
                if (self.preset == 0):    # T(x,y) = sin(x)
                    for i in np.arange(nx+2):
                        self.T[i,:,0] = np.sin(i*h)
                elif (self.preset == 1):    # T(x,y) = x * y
                    for i in np.arange(nx+2):
                        for j in np.arange(ny+2):
                            self.T[i,j,0] = i*j*h**2
                elif (self.preset == 2):    # Hot pyramid
                    for j in np.arange(ny+2):
                        for i in np.arange(nx+2):
                            if (i >= j and i <= (nx+1-j)):
                                self.T[i,j,0] = 100
                elif (self.preset == 3):    # Hot circle
                    if (nx < ny): r = (nx+2)/3
                    else: r = (ny+2)/3
                    for r in range(int(r)):
                        for angle in range(360):
                            x = r * np.sin(np.radians(angle)) + (nx)/2
                            y = r * np.cos(np.radians(angle)) + (ny)/2
                            x = int(round(x))
                            y = int(round(y))
                            self.T[x,y,0] = 100

        def boundary(self):
            k = self.k
            lDir = self.lDir
            rDir = self.rDir
            bDir = self.bDir
            tDir = self.tDir
            
            # Neumann (insulated) boundary conditions by default
            self.T[0,:,k] = self.T[1,:,k]  # Left border = neighbor temp
            self.T[nx+1,:,k] = self.T[nx,:,k]  # Right border = neighbor temp
            self.T[:,0,k] = self.T[:,1,k]  # Bottom border = neighbor temp
            self.T[:,ny+1,k] = self.T[:,ny,k]  # Top border = neighbor temp
        
            # Dirichlet conditions
            if lDir:
                self.T[0,:,k] = self.lTemp
            if rDir:
                self.T[nx+1,:,k] = self.rTemp
            if bDir:
                self.T[:,0,k] = self.bTemp
            if tDir:
                self.T[:,ny+1,k] = self.tTemp

        # User selected region and temperature
        def areaTemp(self):
            region = self.region
            region_temp = self.region_temp
            self.T[int(region[0]/h)+1:int(region[1]/h)+2,
                   int(region[2]/h)+1:int(region[3]/h)+2,0] = region_temp

        initPlate(self)

        if custom_region: areaTemp(self)
            
        boundary(self)    
        
        # Progress bar tk widget
        gui.progress = ttk.Progressbar(gui.root,orient=tk.HORIZONTAL,
                                       length=200,mode='determinate')
                                       
        gui.progress.grid(row=(gui.r-1),column=1,columnspan=2)
        gui.progress["maximum"] = nt-2
    
        a_dt_h2 = (a * dt) / (h ** 2) # Moved as many operations as I could
                                      # outside the computation loop
    
        for t in range(nt-1):
            self.k = t
            boundary(self)
            
            gui.progress["value"] = t
            gui.progress.update_idletasks()   # Update progress bar immediately
            
# Algorithm utilizes finite-difference method to solve for the future
# temperature of a region, based on its current temperature and the temperature
# of the four bordering regions. I'd like to thank the resource below for
# helping me to understand and utilize the method:
# http://www.u.arizona.edu/~erdmann/mse350/_downloads/2D_heat_equation.pdf

            for i in range(1,nx+1):
                for j in range(1,ny+1):
                    cur = self.T[i,j,t] # Current value of small region
                    lNbr = self.T[i-1,j,t] # Left neighbor
                    rNbr = self.T[i+1,j,t] # Right neighbor
                    tNbr = self.T[i,j+1,t] # Top neighbor
                    bNbr = self.T[i,j-1,t] # Bottom neighbor
                    
                    # Future value of small region
                    self.T[i,j,t+1] = cur + a_dt_h2*(lNbr+rNbr+bNbr+tNbr-4*cur)

        data = self.T[1:nx+1,1:ny+1,:]
        
        # Switch index convention from matrix to coordinate style for graphing
        self.dFlip = np.flipud(data.transpose(1,0,2))
    
    ###########################################################################
    def animate(self,gui):
        dFlip = self.dFlip
        
        fig = plt.figure()
        ax = fig.add_subplot(111)
        
        # Canvas used to display the animation embedded within a tkinter window
        canvas = FigureCanvasTkAgg(fig, master=gui.root)
        canvas.show()
        canvas.get_tk_widget().grid(row=0,column=12,rowspan=gui.r,
                                    sticky=tk.E+tk.N+tk.S)

        images = []

        for i in range(self.nt):
            im = ax.imshow(dFlip[:,:,i],cmap='hot',animated=True)
            images.append([im])

        ax.set_xlabel("x")
        ax.set_ylabel("y")
        plt.xticks(np.linspace(0,self.nx-1,6), np.linspace(0,self.Lx,6))
        plt.yticks(np.linspace(self.ny-1,0,6), np.linspace(0,self.Ly,6))

        # Allowing animations to repeat causes big stability problems. I was
        # sadly unable to fix this and implement it as a user selectable option
        gui.anim = animation.ArtistAnimation(fig,images,interval=0,blit=True,
                                  repeat=0)

        canvas.show()

###############################################################################
# Main program loop
###############################################################################
root = tk.Tk()
gui = GUI(root)
root.mainloop()
