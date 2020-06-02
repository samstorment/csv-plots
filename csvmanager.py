import csv

class CSV:
    def __init__(self, filename):
        self.filename = filename
        self.colDict = {}
        self.colArr = []
        self.numRows = self.loadColNames()

    def loadColNames(self):
        with open(self.filename) as file:
            reader = csv.reader(file, delimiter=',')
            rowCount = 0
            for row in reader:
                if rowCount == 0:
                    colCount = 0
                    for col in row:
                        self.colDict[col] = colCount
                        self.colArr.append(col)
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
                    colNum = self.colDict[colName]

                    value = row[colNum]
                    if value == '' or value == '--':
                        value = 0.0
                    elif colName == 'Name':
                        value = value.split('\\')[0]
                    else:
                        value = float(value)

                    colArray.append(value)
            return colArray

