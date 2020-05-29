import csv

colDict = {}
colArr = []
colName = []

def loadColNames(filename):
    with open(filename) as file:
        reader = csv.reader(file, delimiter=',')
        rowCount = 0
        for row in reader:
            if rowCount == 0:
                colCount = 0
                for col in row:
                    colDict[col] = colCount
                    colArr.append(col)
                    colCount += 1
            rowCount += 1
        return colArr

def getAllCol(filename, colName, numRows):
    colArray = []
    with open(filename) as file:
        reader = csv.reader(file, delimiter=',')
        rowCount = 0
        for row in reader:
            rowCount += 1
            if rowCount > 1 and rowCount < numRows:
                colNum = colDict[colName]

                value = row[colNum]
                if value == '':
                    value = 0.0
                elif colName == 'Name':
                    value = value.split('\\')[0]
                else:
                    value = float(value)

                colArray.append(value)
        return colArray

# testing
# filename = 'japan.csv'
# numRows = loadColNames(filename)
# war = getAllCol(filename, 'WAR', numRows)