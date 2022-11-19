import pandas as pd
from functools import reduce, partial



def checkKeyName(key,frame, name):
    return frame[key].str.contains(name)

def AndBoolSeries(seriesList):
    singleAnd = lambda x, y: (x) & (y)
    return reduce(singleAnd, seriesList)

def OrBoolSeries(seriesList):
    singleOr = lambda x, y: (x) | (y)
    return reduce(singleOr, seriesList)

def NorBoolSeries(seriesList):
    singleNor = lambda x, y: ~(x) & ~(y)
    return (reduce(singleNor, seriesList))

def checkManyKeyNames(checkKeyNameFunc, frame, andList, orList, exclList):
    finalSeriesList = []
    if len(andList) != 0:
        andSeries = AndBoolSeries([checkKeyNameFunc(frame, andTerm) for andTerm in andList])
        finalSeriesList.append(andSeries)
    if len(orList) != 0:
        orSeries = OrBoolSeries([checkKeyNameFunc(frame, orTerm) for orTerm in orList])
        finalSeriesList.append(orSeries)
    if len(exclList) != 0:
        exclSeries = NorBoolSeries([checkKeyNameFunc(frame, exclTerm) for exclTerm in exclList])
        finalSeriesList.append(exclSeries)

    completeSeries = AndBoolSeries(finalSeriesList)
    return frame[completeSeries]

def processCalgary():
    checkName = partial(checkKeyName, 'TRADENAME')
    checkManyNames = partial(checkManyKeyNames, checkName)

    calFrame = pd.read_csv("rawdata/calgaryData.csv")
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

def processEdmonton():
    edmFrame = pd.read_csv("rawdata/edmontonData.csv")
    checkName = partial(checkKeyName, 'Trade Name')
    checkManyNames = partial(checkManyKeyNames, checkName)
    foodFrame = edmFrame[(edmFrame['Category'] == 'Major Retail Store')]

    rcssFrame = checkManyNames(foodFrame, ['CANADIAN SUPERSTORE'], [], [])
    safewayFrame = checkManyNames(foodFrame, ['SAFEWAY'], [], ['SAFEWAY GAS', 'SAFEWAY LIQUOR'])
    walmartFrame = checkManyNames(foodFrame, ['WAL-MART'], [], [])
    sobeysFrame = checkManyNames(foodFrame, ['SOBEYS'], [], [])
    coopFrame = checkManyNames(foodFrame, ['CO-OP'], [], ['CO-OP WINE', 'GAS BAR'])
    supermarketFrame = checkManyNames(foodFrame, ['SUPERMARKET'], [], [])
    martFrame = checkManyNames(foodFrame, ['GROCER'],[],[])

    finalEdmonton = pd.concat([rcssFrame,
                              safewayFrame,
                              walmartFrame,
                              sobeysFrame,
                              coopFrame,
                              supermarketFrame,
                              martFrame],axis=0)
    #print(finalEdmonton['Trade Name'])
    #print(len(finalEdmonton.index))
    #print(len(foodFrame.index))
    finalEdmonton.to_csv('cleandata/edmonton.csv', index=False)
processEdmonton()
processCalgary()

