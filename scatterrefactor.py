# A refactor of baseballscatter.py

import tkinter as tk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from tkinter.filedialog import askopenfilename
from tkinter import colorchooser
from functools import partial
import csv
import color
import os


# Class for managing a tkinter window with embedded scatter plot. Class name could probably be changed to something more generic since these functions are specific to scatter plots
class Scatter:
    def __init__(self, root):
        self.root = root
    
    # create a scatter plot nested inside a tkinter window from the given lists
    def scatter(self, x=[], y=[]):
        figure = Figure()
        plot = figure.add_subplot(111)
        plot.scatter(x, y)
        canvas = FigureCanvasTkAgg(figure, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)
        toolbar = NavigationToolbar2Tk(canvas, self.root)
        toolbar.update()
        return figure, plot, canvas

    # instead of having a sidebar and sidebarROw, could just make a frame method with more parameters
    def sidebar(self, barside=tk.RIGHT, barcolor='white'):
        sidebar = tk.Frame(self.root, bg=barcolor)
        sidebar.pack(expand=0, fill='y', side=barside)
        return sidebar
    
    def sidebarRow(self, parent, color='white', padx=0, pady=0):
        sidebarRow = tk.Frame(parent, bg=color)
        sidebarRow.pack(expand=0, fill='both', padx=padx, pady=pady)
        return sidebarRow

    def button(self, parent, text=None, width=10, color='white', side=tk.LEFT, padx=5, pady=5, command=None):
        button = tk.Button(parent, text=text, width=width, bg=color, command=command)
        button.pack(side=side, padx=padx, pady=pady)
        return button
        
    def label(self, parent, text=None, width=10, color='white', side=tk.LEFT, padx=5, pady=5, txtvar=None):
        label = tk.Label(parent, text=text, width=width, bg=color, textvariable=txtvar)
        label.pack(side=side, padx=padx, pady=pady)
        return label

    def entry(self, parent, width=30, color='white', side=tk.RIGHT, padx=5, pady=5, txtvar=None):
        entry = tk.Entry(parent, width=width, bg=color, textvariable=txtvar)
        entry.pack(side=side, padx=padx, pady=pady)
        return entry

    def dropdown(self, parent, txtvar, options, side=tk.RIGHT, padx=5, pady=5, defaultval=''):
        txtvar.set(defaultval)
        dropdown = tk.OptionMenu(parent, txtvar, *options)
        dropdown.pack(side=side, padx=padx, pady=pady)
        return dropdown

    def checkbox(self, parent, intvar, text=None, width=10, color='white', side=tk.LEFT, padx=5, pady=5):
        intvar.set(0)
        checkbox = tk.Checkbutton(parent, variable=intvar, text=text, width=width, bg=color, onvalue=1, offvalue=0)
        checkbox.pack(side=side, padx=padx, pady=pady)
        return checkbox

    # changes the options in an option menu to the values in the given option list
    def changeDropdown(self, dropdown, txtvar, options):
        # delete all the options from the dropdown menu
        dropdown.children['menu'].delete(0, 'end')
        txtvar.set('')
        # for each option in the new list, add the option to the drop down and set the dropmenu's text as to the option if chosen
        for o in options:
            dropdown.children['menu'].add_command(label=o, command=lambda opt=o: txtvar.set(opt))
    
    # changes the title text and color for the given plot
    def changeTitle(self, plot, text, color):
        plot.set_title(text, size='24', pad=20, color=color)
        plot.spines['top'].set_color(color)
        plot.spines['bottom'].set_color(color)
        plot.spines['left'].set_color(color)
        plot.spines['right'].set_color(color)

    # changes the label text and color for the given plot on the given axis
    def changeLabel(self, plot, axis, text, color):
        if axis == 'x':
            plot.set_xlabel(text, size='16', labelpad=20, color=color)
            plot.tick_params(axis='x', colors=color)
        elif axis == 'y':
            plot.set_ylabel(text, size='16', labelpad=20, color=color)
            plot.tick_params(axis='y', colors=color)

    # updates button text and color to the selected color, assigns the selected color to the StrVar so we can use it to change more colors when we submit
    def colorBtnClick(self, txtvar, btn):
        col = tk.colorchooser.askcolor()[1]
        txtvar.set(col)
        btn.configure(bg=col, text=col, fg=color.invert(col, 1))

    # 
    def fileBtnClick(self, txtvar, label):
        filepath = askopenfilename()
        txtvar.set(filepath)
        filename = os.path.basename(filepath)
        label.configure(text=filename)

def main():

    root = tk.Tk()
    s = Scatter(root)

    sidebar = s.sidebar()
    fig, plt, canv = s.scatter()
    
    filerow = s.sidebarRow(sidebar)
    filepath = tk.StringVar()
    filelabel = s.label(filerow, width=35, color='lightgray', side=tk.RIGHT)
    s.button(filerow, 'CSV:', width=6, command=partial(s.fileBtnClick, filepath, filelabel))

    titlerow = s.sidebarRow(sidebar)
    titlecolor = tk.StringVar()
    s.label(titlerow, 'Title', color='lightgray', width=7)
    s.entry(titlerow, side=tk.LEFT)
    titlebtn = s.button(titlerow, '#ffffff', width=7, side=tk.RIGHT, color='white')
    titlebtn.configure(command=partial(s.colorBtnClick, titlecolor, titlebtn))

    xaxisrow = s.sidebarRow(sidebar)
    xaxiscolor = tk.StringVar()
    s.label(xaxisrow, 'X-Axis', color='lightgray', width=7)
    s.entry(xaxisrow, side=tk.LEFT)
    xaxisbtn = s.button(xaxisrow, '#ffffff', width=7, side=tk.RIGHT, color='white')
    xaxisbtn.configure(command=partial(s.colorBtnClick, xaxiscolor, xaxisbtn))

    yaxisrow = s.sidebarRow(sidebar)
    yaxiscolor = tk.StringVar()
    s.label(yaxisrow, 'Y-Axis', color='lightgray', width=7)
    s.entry(yaxisrow, side=tk.LEFT)
    yaxisbtn = s.button(yaxisrow, '#ffffff', width=7, side=tk.RIGHT, color='white')
    yaxisbtn.configure(command=partial(s.colorBtnClick, yaxiscolor, yaxisbtn))


    root.mainloop()

    # some test prints
    print(filepath.get())
    print(yaxiscolor.get())


main()