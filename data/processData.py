import pandas as pd
from functools import reduce

# Load Data
calFrame = pd.read_csv("rawdata/calgaryData.csv")
edmFrame = pd.read_csv("rawdata/edmontonData.csv")

def checkName(frame, name):
    return frame['TRADENAME'].str.contains(name)

def AndBoolSeries(seriesList):
    singleAnd = lambda x, y: (x) & (y)
    return reduce(singleAnd, seriesList)

def OrBoolSeries(seriesList):
    singleOr = lambda x, y: (x) | (y)
    return reduce(singleOr, seriesList)

def NorBoolSeries(seriesList):
    singleNor = lambda x, y: ~(x) & ~(y)
    return (reduce(singleNor, seriesList))

def checkManyNames(frame, andList, orList, exclList):
    finalSeriesList = []
    if len(andList) != 0:
        andSeries = AndBoolSeries([checkName(frame, andTerm) for andTerm in andList])
        finalSeriesList.append(andSeries)
    if len(orList) != 0:
        orSeries = OrBoolSeries([checkName(frame, orTerm) for orTerm in orList])
        finalSeriesList.append(orSeries)
    if len(exclList) != 0:
        exclSeries = NorBoolSeries([checkName(frame, exclTerm) for exclTerm in exclList])
        finalSeriesList.append(exclSeries)

    completeSeries = AndBoolSeries(finalSeriesList)
    return frame[completeSeries]

foodCategory = calFrame['LICENCETYPES'] == "FOOD SERVICE - PREMISES"
foodFrame = calFrame[foodCategory]

rcssFrame = checkManyNames(foodFrame, ['CANADIAN SUPERSTORE'], [], [])
safewayFrame = checkManyNames(foodFrame, ['SAFEWAY'], [], ['SAFEWAY GAS', 'SAFEWAY LIQUOR'])
walmartFrame = checkManyNames(foodFrame, ['WAL-MART'], [], [])
sobeysFrame = checkManyNames(foodFrame, ['SOBEYS'], [], [])
coopFrame = checkManyNames(foodFrame, ['CO-OP'], [], ['CO-OP WINE', 'GAS BAR'])
supermarketFrame = checkManyNames(foodFrame, ['SUPERMARKET'], [], [])
martFrame = checkManyNames(foodFrame, ['GROCER'],[],[])

finalCalgary = pd.concat([rcssFrame,
                          safewayFrame,
                          walmartFrame,
                          sobeysFrame,
                          coopFrame,
                          supermarketFrame,
                          martFrame],axis=0)
finalCalgary.to_csv('cleandata/calgary.csv',index=False)