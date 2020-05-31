# A refactor of baseballscatter.py

import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import colorchooser
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from functools import partial
import csvmanager as csv
import color as clr
import os
from typing import NamedTuple


class Vec3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class Graph(NamedTuple):
    figure: Figure
    plot: object    # specific type = matplotlib.axes._subplots.AxesSubplot object
    canvas: FigureCanvasTkAgg


# Class for managing a tkinter window with embedded scatter plot. Class name could probably be changed to something more generic since these functions are specific to scatter plots
class Scatter:
    def __init__(self, root):
        self.root = root
        self.graph = None
        self.csvfile = None
    
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
        self.graph = Graph(figure, plot, canvas)

    # Helps me visualize frames as html divs
    def div(self, parent, color='#ffffff', side=tk.TOP, padx=0, pady=0, fill='both'):
        sidebar = tk.Frame(parent, bg=color)
        sidebar.pack(expand=0, fill=fill, side=side, padx=padx, pady=pady)
        return sidebar

    def button(self, parent, text=None, width=10, color='#ffffff', side=tk.LEFT, padx=5, pady=5, command=None):
        button = tk.Button(parent, text=text, width=width, bg=color, fg=clr.invert(color, 1), command=command)
        button.pack(side=side, padx=padx, pady=pady)
        return button
        
    def label(self, parent, text=None, width=10, color='#d3d3d3', side=tk.LEFT, padx=5, pady=5, txtvar=None):
        label = tk.Label(parent, text=text, width=width, bg=color, fg=clr.invert(color, 1), textvariable=txtvar)
        label.pack(side=side, padx=padx, pady=pady)
        return label

    def entry(self, parent, width=35, color='#ffffff', side=tk.LEFT, padx=5, pady=5, txtvar=None):
        entry = tk.Entry(parent, width=width, bg=color, textvariable=txtvar)
        entry.pack(side=side, padx=padx, pady=pady)
        return entry

    def dropdown(self, parent, txtvar, options=[''], side=tk.LEFT, padx=5, pady=5, defaultval=''):
        txtvar.set(defaultval)
        dropdown = tk.OptionMenu(parent, txtvar, *options)
        dropdown.pack(side=side, padx=padx, pady=pady)
        return dropdown

    def checkbox(self, parent, intvar, text=None, width=10, color='#ffffff', side=tk.LEFT, padx=5, pady=5):
        intvar.set(0)
        checkbox = tk.Checkbutton(parent, variable=intvar, text=text, width=width, bg=color, onvalue=1, offvalue=0)
        checkbox.pack(side=side, padx=padx, pady=pady)
        return checkbox

    def colorRow(self, parent, clrvar, label, initclr):
        clrrow = self.div(parent)
        clrvar.set(initclr)
        self.label(clrrow, label, width=15)
        clrbtn = self.button(clrrow, initclr, side=tk.RIGHT, color=initclr)
        clrbtn.configure(command=partial(self.colorBtnClick, clrvar, clrbtn))

    # changes the options in an option menu to the values in the given option list
    def changeDropdown(self, dropdown, txtvar, options):
        # delete all the options from the dropdown menu
        dropdown.children['menu'].delete(0, 'end')
        txtvar.set('')
        # for each option in the new list, add the option to the drop down and set the dropmenu's text as to the option if chosen
        for o in options:
            dropdown.children['menu'].add_command(label=o, command=lambda opt=o: txtvar.set(opt))
    
    # changes the title text and color for the given plot
    def changeTitle(self, entries, color):
        self.graph.plot.set_title(entries.z.get(), size='24', pad=20, color=color)
        self.graph.plot.spines['top'].set_color(color)
        self.graph.plot.spines['bottom'].set_color(color)
        self.graph.plot.spines['left'].set_color(color)
        self.graph.plot.spines['right'].set_color(color)

    # changes the label text and color for the given plot on the given axis
    def changeLabel(self, entries, color):
        self.graph.plot.set_xlabel(entries.x.get(), size='16', labelpad=20, color=color)
        self.graph.plot.tick_params(axis='x', colors=color)
        self.graph.plot.set_ylabel(entries.y.get(), size='16', labelpad=20, color=color)
        self.graph.plot.tick_params(axis='y', colors=color)

    def addDataLabels(self, datavars, color, optionlists):

        datalbloption = datavars.z.get()

        xlist = optionlists.x
        ylist = optionlists.y

        if datalbloption != '':
            datalabels = self.csvfile.getAllCol(datalbloption)
            for i in range(len(datalabels)):
                self.graph.plot.annotate(datalabels[i], (xlist[i], ylist[i]), color=color)

    # updates button text and color to the selected color, assigns the selected color to the StrVar so we can use it to change more colors when we submit
    def colorBtnClick(self, txtvar, btn):
        color = tk.colorchooser.askcolor()[1] # subscipt of 1 gives us the hex value rather than rgb
        txtvar.set(color)
        btn.configure(bg=color, text=color, fg=clr.invert(color, 1))


    def fileBtnClick(self, label, dropdowns, datavars):
        filepath = askopenfilename()
        filename = os.path.basename(filepath)

        self.csvfile = csv.CSV(filepath)
        options = self.csvfile.colArr
        self.changeDropdown(dropdowns.x, datavars.x, options)
        self.changeDropdown(dropdowns.y, datavars.y, options)
        self.changeDropdown(dropdowns.z, datavars.z, options)

        label.configure(text=filename)

    def submitBtnCLick(self, entries, datavars, colors, showlabels):

        bgclr = colors[0].get()
        graphclr = colors[1].get()
        pointclr = colors[2].get()
        datalblclr = colors[3].get()
        txtclr = clr.invert(bgclr, 1)
    
        xoption = datavars.x.get()
        yoption = datavars.y.get()
        xlist = []
        ylist = []


        self.graph.plot.clear()

        self.changeTitle(entries, txtclr)
        self.changeLabel(entries, txtclr)

        self.graph.figure.patch.set_facecolor(bgclr)
        self.graph.plot.set_facecolor(graphclr)

        if xoption != '' and yoption != '':
            xlist = self.csvfile.getAllCol(xoption)
            ylist = self.csvfile.getAllCol(yoption)
            optionlists = Vec3(xlist, ylist, None)
            if showlabels.get():
                self.addDataLabels(datavars, datalblclr, optionlists)

        self.graph.plot.scatter(xlist, ylist, color=pointclr)

        self.graph.canvas.draw()


def main():

    root = tk.Tk()
    s = Scatter(root)

    sidebar = s.div(root, side=tk.RIGHT)
    s.scatter()
    
    filerow = s.div(sidebar)
    filebutton = s.button(filerow, 'CSV:')
    filelabel = s.label(filerow, width=30)

    titlerow = s.div(sidebar)
    s.label(titlerow, 'Title')
    titleentry = s.entry(titlerow, side=tk.RIGHT)

    xlblrow = s.div(sidebar)
    s.label(xlblrow, 'X-Label')
    xentry = s.entry(xlblrow, side=tk.RIGHT)

    ylblrow = s.div(sidebar)
    s.label(ylblrow, 'Y-Label')
    yentry = s.entry(ylblrow, side=tk.RIGHT)

    entries = Vec3(xentry, yentry, titleentry)

    xdatavar = tk.StringVar()
    xdatarow = s.div(sidebar)
    s.label(xdatarow, 'X-Data')
    xdropdown = s.dropdown(xdatarow, xdatavar, side=tk.RIGHT)

    ydatavar = tk.StringVar()
    ydatarow = s.div(sidebar)
    s.label(ydatarow, 'Y-Data')
    ydropdown = s.dropdown(ydatarow, ydatavar, side=tk.RIGHT)


    bgclrvar = tk.StringVar()
    s.colorRow(sidebar, bgclrvar, 'Background Color', '#ffffff')

    graphclrvar = tk.StringVar()
    s.colorRow(sidebar, graphclrvar, 'Graph Color', '#ffffff')

    pointclrvar = tk.StringVar()
    s.colorRow(sidebar, pointclrvar, 'Point Color', '#0000ff')

    datalblclrvar = tk.StringVar()
    s.colorRow(sidebar, datalblclrvar, 'Data Label Color', '#ff00cc')

    datalblvar = tk.StringVar()
    datacheckvar = tk.IntVar()
    datalblrow = s.div(sidebar)
    s.label(datalblrow, 'Data Labels')
    datalbldropdown = s.dropdown(datalblrow, datalblvar, side=tk.RIGHT)
    s.checkbox(datalblrow, datacheckvar, 'Show')



    colors = [bgclrvar, graphclrvar, pointclrvar, datalblclrvar]
    dropdowns = Vec3(xdropdown, ydropdown, datalbldropdown)
    datavars = Vec3(xdatavar, ydatavar, datalblvar)
    filebutton.configure(command=partial(s.fileBtnClick, filelabel, dropdowns, datavars))


    submitrow = s.div(sidebar)
    s.button(submitrow, 'Submit', width=10, side=tk.RIGHT, command=partial(s.submitBtnCLick, entries, datavars, colors, datacheckvar))
    root.bind('<Return>', lambda e=None : s.submitBtnCLick(entries, datavars, colors, datacheckvar))

    root.mainloop()

main()