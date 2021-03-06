# !/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import division
import ctypes
import sys
import os

if eval(sys.version[0]) < 3: # For check python version
    raise ValueError('GUI code requires python3 or higher')
else:
    from tkinter import *
sys.path.append("..")

from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from matplotlib.figure import Figure
import matplotlib.image as mpimg
from rk4 import firstorder
import numpy as np
import sympy
(t, y, e) = sympy.symbols("t, y, e")

class GUI:
    def __init__(self, master):
        # Window design
        self.master = master
        gui_bg = "#4F5251"
        master.title("Runge Kutta 4th Order")
        master.config(bg=gui_bg)
        master.geometry("1200x600")
        master.resizable(width=FALSE, height=FALSE)

        # Detect OS for icon
        self.OS = sys.platform
        if self.OS == 'linux' or 'darwin':
            icon = PhotoImage(file='images/RK4-logo.png')
            master.tk.call('wm', 'iconphoto', master._w, icon)
        if self.OS == 'win32':
            # For Windows system show icon
            master.wm_iconbitmap(default='images/RK4-logo.ico')
            myappid = 'Isa-Carlos.RungeKutta.RK4.1-1'  # arbitrary string
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        # Initialize graph parameters
        self.fig = Figure(figsize=(7, 4), dpi=110, facecolor=gui_bg)
        self.fig.clf()
        self.ax = self.fig.add_subplot(111, facecolor=gui_bg)
        self.canvas = FigureCanvasTkAgg(self.fig, self.master)
        self.canvas.get_tk_widget().place(x=450, y=100)
        self.canvas.draw()

        titletext = Label(master, text="Runge Kutta 4th Order",
                          bg=gui_bg, fg="white", font="time 20 bold")
        titletext.pack(side='top')

        titleODE = Label(master, text="Ordinary differential equations of the first order",
                         bg=gui_bg, fg="white", font="time 12 bold").place(x=90, y=40)

        label_equation = Label(master, text='Enter equation: dy/dt =',
                               bg='#689E8C').place(x=110, y=80, width=180, height=40)

        self.ts = self.ys = []
        self.equation = StringVar()
        self.equation.set('2 * t - 3 * y + 1')
        equantion_entry = Entry(master, width=12,
                                textvariable=self.equation).place(x=290, y=80, width=150, height=40)

        self.label_parameters = Label(master, text='Parameters',
                                      bg='#476B5F').place(x=225, y=130, width=100, height=40)

        # ti parameter
        self.label_ti = Label(master, text='ti :',
                              bg='#689E8C').place(x=110, y=170, width=40, height=25)
        self.ti = DoubleVar()
        self.ti.set('1.0')
        self.entry_ti = Entry(master, width=7,
                              textvariable=self.ti).place(x=150, y=170, width=40, height=25)

        # yi parameter
        self.label_yi = Label(master, text='yi :',
                              bg='#689E8C').place(x=190, y=170, width=40, height=25)
        self.yi = DoubleVar()
        self.yi.set('5.0')
        self.entry_yi = Entry(master, width=7,
                              textvariable=self.yi).place(x=220, y=170, width=40, height=25)

        # t parameter
        self.label_t = Label(master, text='t :',
                             bg='#689E8C').place(x=260, y=170, width=40, height=25)
        self.t = DoubleVar()
        self.t.set('1.5')
        self.entry_t = Entry(master, width=7,
                             textvariable=self.t).place(x=300, y=170, width=40, height=25)

        # h parameter
        self.label_h = Label(master, text='h :', bg='#689E8C').place(x=340, y=170, width=40, height=25)
        self.h = DoubleVar()
        self.h.set('0.01')
        self.entry_h = Entry(master, width=7, textvariable=self.h).place(x=380, y=170, width=40, height=25)

        # computed
        compute = Button(master, text='Compute', command=self.solve, relief='raised',
                         bg='#989E9C').place(x=180, y=200, width=80, height=30)

        self.computed = DoubleVar()
        self.label_computed = Label(master, textvariable=self.computed,
                                    width=20).place(x=260, y=200, width=150, height=30)

        # Graph
        graph_label = Label(master, text='Solution graph',
                            bg="#4F5251", fg="white", font="time 14 bold").place(x=790, y=40)
        graph_button = Button(master, text='Graph', command=self.graph,
                              relief='raised', bg='#989E9C').place(x=770, y=80, width=200, height=20)

        self.button_close = Button(master, text='Close', bg='#E1EBE7', fg="black",
                                   command=self.exit).place(x=1100, y=550, width=80, height=30)

    def f(self, t, y):
        """
        Declare function to solve in the RK4 library format.

        Parameters
        ----------
        t : Variable needed for the function imported from RK4.
        y : Variable needed for the function imported from RK4.

        Return
        ------
        ODE : Evaluation of the function entered in the GUI to be solved.
        """

        ODE = eval(self.equation.get())
        return ODE

    def solve(self):
        """
        To use the -solve- function of RK4 and solve the equation that was
        entered in the GUI
        """

        # Initialize Runge-Kutta firstorder ode
        methd = firstorder(self.f)
        r = methd.solve(np.double(self.ti.get()), np.double(self.yi.get()),
                        np.double(self.t.get()), np.double(self.h.get()))
        # Obtain values of solution
        self.ts, self.ys = methd.get_vals()
        self.computed.set(r)

    def graph(self):
        """
        Graph values of each iteration of method
        """

        if len(self.ts) == 0 or len(self.ts) == 0:
            raise ValueError('You need to press computed first')

        self.ax.clear()
        self.ax.set_title(r'ODE: $\frac{dy}{dt}= %s$' % sympy.latex(eval(self.equation.get())))
        self.ax.plot(self.ts, self.ys, '--r', label='Solution curve')
        yevalxstr = r'$ y({}) $'.format(self.t.get())
        self.ax.scatter(self.ts[len(self.ts) - 1], self.ys[len(self.ys) - 1],
                        facecolor='k', label=yevalxstr)
        self.ax.legend()
        self.ax.grid()
        self.ax.set_xlabel("$ t $")
        self.ax.set_ylabel("$ y(t) $", rotation='horizontal', fontsize='large')

        self.canvas.draw()

    def exit(self):
        """
        Finish the GUI
        """

        self.master.quit()
        sys.exit()

def main():
    root = Tk()
    rk = GUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
