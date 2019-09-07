#!/usr/bin/env python3

#
# Written by Chase Hill 2019
#

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import animation
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import ttk

from gui import gui

class simulator(GUI):
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

            cur = self.T[:,:,t]             # Current value of grid
            rollL = np.roll(cur,1,axis=1)   # Roll the grid left
            rollR = np.roll(cur,-1,axis=1)  # Roll the grid right
            rollU = np.roll(cur,1,axis=0)   # Roll the grid up
            rollD = np.roll(cur,-1,axis=0)  # Roll the grid down

            # Future grid values computed
            self.T[:,:,t+1] = cur + a_dt_h2*(rollL+rollR+rollU+rollD-4*cur)

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
