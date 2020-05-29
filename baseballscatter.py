import tkinter as tk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from tkinter.filedialog import askopenfilename
from tkinter import colorchooser
from functools import partial
import csv


class CSV:
    def __init__(self, filename):
        self.filename = filename
        self.columns = {}
        self.colName = []
        self.numRows = self.loadColNames()

    def loadColNames(self):
        with open(self.filename) as file:
            reader = csv.reader(file, delimiter=',')
            rowCount = 0
            for row in reader:
                if rowCount == 0:
                    colCount = 0
                    for col in row:
                        self.columns[col] = colCount
                        colCount += 1
                rowCount += 1
            return rowCount

    def getAllCol(self, colName):
        colArray = []
        with open(self.filename) as file:
            reader = csv.reader(file, delimiter=',')
            rowCount = 0
            for row in reader:
                rowCount += 1
                if rowCount > 1 and rowCount < self.numRows:
                    colNum = self.columns[colName]

                    value = row[colNum]
                    if value == '':
                        value = 0.0
                    elif colName == 'Name':
                        value = value.split('\\')[0]
                    else:
                        value = float(value)

                    colArray.append(value)
            return colArray



class Scatter:
    def __init__(self, root):

        self.csv = None
        self.annotate = tk.IntVar()

        self.x = ['None']
        self.y = ['None']

        self.defaultX = tk.StringVar()
        self.defaultY = tk.StringVar()

        self.outsideColor = tk.StringVar()
        self.outsideColor.set('white')
        self.plotColor = tk.StringVar()
        self.plotColor.set('white')
        self.pointColor = tk.StringVar()
        self.pointColor.set('blue')
        self.annotateColor = tk.StringVar()
        self.annotateColor.set('red')

        self.filepath = ''
        self.filename = tk.StringVar()

        self.sidebar = self.setSidebar(root)
        self.figure, self.plot = self.setPlot(self.x, self.y)
        self.canvas = self.setCanvas(self.figure)

        fileButtonRow = self.sidebarRow(self.sidebar)
        self.fileButtonLabel = self.sidebarLabel(fileButtonRow, 10, self.filename)
        self.sidebarButton(fileButtonRow, 'CSV File:', 15,  self.fileButtonClick)

        # self.sidebarButton(self.sidebar, 'Choose a csv file', 50, self.fileButtonClick)

        # csvLabelRow = self.sidebarRow(self.sidebar)
        # self.csvText = self.sidebarText(csvLabelRow, 'File:', self.filename)

        titleRow = self.sidebarRow(self.sidebar)
        self.titleEntry = self.sidebarEntry(titleRow, 'Title')

        xlabelRow = self.sidebarRow(self.sidebar)
        self.xlabelEntry = self.sidebarEntry(xlabelRow, 'X-Title')

        ylabelRow = self.sidebarRow(self.sidebar)
        self.ylabelEntry = self.sidebarEntry(ylabelRow, 'Y-Title')

        xdataRow = self.sidebarRow(self.sidebar)
        self.xdataDropdown = self.sidebarDropdown(xdataRow, 'X-Col', self.x, self.defaultX, 0)

        ydataRow = self.sidebarRow(self.sidebar)
        self.ydataDropdown = self.sidebarDropdown(ydataRow, 'Y-Col', self.y, self.defaultY, 0)

        self.sidebarCheckbox(self.sidebar, "Show Annotations")

        outsideColorRow = self.sidebarRow(self.sidebar)
        self.outsideColorLabel = self.sidebarLabel(outsideColorRow, 10, self.outsideColor)
        self.sidebarButton(outsideColorRow, 'Outside Color', 15,  partial(self.colorButtonClick, self.outsideColor, self.outsideColorLabel))

        plotColorRow = self.sidebarRow(self.sidebar)
        self.plotColorLabel = self.sidebarLabel(plotColorRow, 10, self.plotColor)
        self.sidebarButton(plotColorRow, 'Plot Color', 15,  partial(self.colorButtonClick, self.plotColor, self.plotColorLabel))

        pointColorRow = self.sidebarRow(self.sidebar)
        self.pointColorLabel = self.sidebarLabel(pointColorRow, 10, self.pointColor)
        self.sidebarButton(pointColorRow, 'Point Color', 15,  partial(self.colorButtonClick, self.pointColor, self.pointColorLabel))

        annotateColorRow = self.sidebarRow(self.sidebar)
        self.annotateColorLabel = self.sidebarLabel(annotateColorRow, 10, self.annotateColor)
        self.sidebarButton(annotateColorRow, 'Annotate Color', 15,  partial(self.colorButtonClick, self.annotateColor, self.annotateColorLabel))

        saveButtonRow = self.sidebarRow(self.sidebar)
        self.sidebarButton(saveButtonRow, 'Save', 50, self.saveButtonClick)

        submitButtonRow = self.sidebarRow(self.sidebar)
        self.sidebarButton(submitButtonRow, 'Submit', 50, self.submitButtonClick)

        self.enterListener(root)

    def setPlot(self, x, y):
        figure = Figure()
        plot = figure.add_subplot()
        plot.scatter(x, y)
        return figure, plot

    def setCanvas(self, figure):
        canvas = FigureCanvasTkAgg(figure, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)
        toolbar = NavigationToolbar2Tk(canvas, root)
        toolbar.update()
        return canvas

    def setSidebar(self, root):
        sidebar = tk.Frame(root, bg='white', relief='raised', borderwidth=2)
        sidebar.pack(expand=0, fill='both', side=tk.RIGHT, anchor='nw')
        return sidebar

    def sidebarRow(self, sidebar):
        sidebarRow = tk.Frame(master=sidebar)
        sidebarRow.pack(expand=0, fill='both', pady=5)
        return sidebarRow

    def sidebarButton(self, sidebarRow, btntext, btnwidth, btncommand):
        button = tk.Button(sidebarRow, command=btncommand, text=btntext, width=btnwidth)
        button.pack(side=tk.LEFT)

    def sidebarLabel(self, sidebarRow, labelwidth, labelvar):
        label = tk.Label(sidebarRow, width=labelwidth, textvariable=labelvar)
        label.pack(side=tk.RIGHT, pady=5, padx=5)
        return label

    def sidebarEntry(self, sidebarRow, label):
        sidebarLabel = tk.Label(master=sidebarRow, text=label, width=5)
        sidebarLabel.pack(side=tk.LEFT, pady=5)
        sidebarEntry = tk.Entry(master=sidebarRow, width=50, borderwidth=4, relief='ridge')
        sidebarEntry.pack(side=tk.TOP, pady=5)
        return sidebarEntry

    def sidebarText(self, sidebarRow, label, var):
        sidebarLabel = tk.Label(master=sidebarRow, text=label, width=5)
        sidebarLabel.pack(side=tk.LEFT, pady=5)
        sidebarText = tk.Label(master=sidebarRow, width=40, textvariable=var)
        sidebarText.pack(side=tk.TOP, pady=5)
        return sidebarText

    def sidebarCheckbox(self, sidebar, label):
        sidebarCheckbox = tk.Checkbutton(master=sidebar, text=label, variable=self.annotate, onvalue=1, offvalue=0, width=48)
        sidebarCheckbox.pack(side=tk.TOP, pady=5)
        return sidebarCheckbox

    def sidebarDropdown(self, sidebarRow, label, dropdownList, var, defaultIndex):
        sidebarLabel = tk.Label(master=sidebarRow, text=label, width=20)
        sidebarLabel.pack(side=tk.LEFT, pady=5)

        var.set(dropdownList[defaultIndex])

        sidebarDropdown = tk.OptionMenu(sidebarRow, var, *dropdownList)
        sidebarDropdown.pack(side=tk.TOP, pady=5)
        return sidebarDropdown

    # ----- EVENT HANDLERS ----- #
    def fileButtonClick(self):
        self.filepath = askopenfilename()
        self.csv = CSV(self.filepath)
        self.xdataDropdown.children['menu'].delete(0, 'end')
        self.ydataDropdown.children['menu'].delete(0, 'end')
        for k in self.csv.columns:
            self.xdataDropdown.children['menu'].add_command(label=k, command=lambda col=k: self.defaultX.set(col))
            self.ydataDropdown.children['menu'].add_command(label=k, command=lambda col=k: self.defaultY.set(col))

        dirs = self.filepath.split('/')
        csvFile = dirs[len(dirs)-1]
        self.filename.set(csvFile)

    def saveButtonClick(self):
        self.figure.savefig('plot', dpi=95, facecolor=self.toRGBA(self.outsideColor.get()), edgecolor='green',
                orientation='portrait', transparent=False)

    def submitButtonClick(self):
        # get the selected options from the dropdown list
        xoption = self.defaultX.get()
        yoption = self.defaultY.get()

        # get the array of column values for the selected x and y options
        xlist = self.csv.getAllCol(xoption)
        ylist = self.csv.getAllCol(yoption)

        # clear the plot so we have a fresh plot to work off of, then set titles and labels
        self.plot.clear()

        outsideTextColor = self.invertColor(self.outsideColor.get(), 1)
        self.plot.set_title(self.titleEntry.get(), size='24', pad=20, color=outsideTextColor)
        self.plot.set_xlabel(self.xlabelEntry.get(), size='16', labelpad=20, color=outsideTextColor)
        self.plot.set_ylabel(self.ylabelEntry.get(), size='16', labelpad=20, color=outsideTextColor)
        self.setOutsideTextColors(self.plot, outsideTextColor)


        # check if annotations checkbox is checked
        if self.annotate.get():
            # get the array of all names, we will use these to annotate
            names = self.csv.getAllCol('Name')
            # annotate each data point with their name
            for i in range(len(names)):
                self.plot.annotate(names[i], (xlist[i], ylist[i]), color=self.annotateColor.get(), size='8')

        # redraw the catter plot for the new data. redraw the canvas for the new titles/labels
        self.plot.scatter(xlist, ylist, color=self.pointColor.get())
        self.plot.set_facecolor(self.plotColor.get())
        self.figure.patch.set_facecolor(self.outsideColor.get())
        self.canvas.draw()

    def enterListener(self, root):
        def submitEvent(e):
            self.submitButtonClick()
        root.bind('<Return>', submitEvent)

    def colorButtonClick(self, colorVar, colorLabel):
        colorVar.set(tk.colorchooser.askcolor()[1])
        colorLabel.config(bg=colorVar.get())
        colorLabel.config(fg=self.invertColor(colorVar.get(), 1))

    def setOutsideTextColors(self, plot, color):
        plot.spines['top'].set_color(color)
        plot.spines['bottom'].set_color(color)
        plot.spines['left'].set_color(color)
        plot.spines['right'].set_color(color)
        plot.tick_params(axis='x', colors=color)
        plot.tick_params(axis='y', colors=color)

    # this method should not live in this class, it shouldnt be the scatter plot's job to manage this
    def invertColor(self, hexStr, bw):

        # if a hex string is of length 1, add a 0 to the front of it
        def hexify(rgb):
            if len(rgb) == 1:
                return '0' + rgb
            else:
                return rgb

        if (hexStr[0] == '#'):
            hexStr = hexStr[slice(1, len(hexStr))]

        # Convert the hex string to corresponding RGB ints
        r = int(hexStr[slice(0,2)], 16) # red is first 2 hex characters
        g = int(hexStr[slice(2,4)], 16) # green is next 2
        b = int(hexStr[slice(4,6)], 16) # blue is last 2

        if (bw):
            if ((r * 0.299 + g * 0.587 + b * 0.114) > 186):
                return '#000000'
            else:
                return '#ffffff'

        r = 255 - r
        g = 255 - g
        b = 255 - b

        r = hex(r)
        r = hexify(r[slice(2, len(r))])
        g = hex(g)
        g = hexify(g[slice(2, len(g))])
        b = hex(b)
        b = hexify(b[slice(2, len(b))])

        rgb = '#'+r+g+b
        return(rgb)

    def toRGBA(self, hexStr):

        if (hexStr[0] == '#'):
            hexStr = hexStr[slice(1, len(hexStr))]

        # Convert the hex string to corresponding RGB ints
        r = int(hexStr[slice(0,2)], 16) # red is first 2 hex characters
        g = int(hexStr[slice(2,4)], 16) # green is next 2
        b = int(hexStr[slice(4,6)], 16) # blue is last 2

        return (r/255, g/255, b/255, 1)



root = tk.Tk()
root.wm_title("Scatter Plot")
root.state('zoomed')

scatter = Scatter(root)

root.mainloop()
print(scatter.filepath)