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

class gui(object):
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
                        +"functional as possible.\n\nChase Hill - 2019"
        
        tk.Message(top, text=about_message, padx=10, pady=10).grid()
        
        dismiss_button = tk.Button(top, text="Dismiss", command=top.destroy)
        dismiss_button.grid()

    ###########################################################################
    def run(self):
        simulation = simulator(self)
        simulation.compute(self)
        simulation.animate(self)