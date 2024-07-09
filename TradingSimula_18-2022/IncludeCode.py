includeCodeDict = '''def unPackDict(aDict):
    global mp, todaysCTE,curShares,cumuProfit,barsSinceEntry,entryPrice,entryQuant,\
    sectorTradesTodayList,curSector
    mp = aDict.get("mp")
    todaysCTE = aDict.get("todaysCTE")
    curShares = aDict.get("curShares")
    cumuProfit = aDict.get("cumuProfit")
    barsSinceEntry = aDict.get("barsSinceEntry")
    entryPrice = aDict.get("entryPrice")
    entryQuant = aDict.get("entryQuant")'''


includeImports = '''from getData import *
from equityDataClass import *
from tradeClass import *
from systemMarket import *
from indicators import highest,lowest,rsiClass,stochClass,sAverage,bollingerBands,\
    adxClass,sAverage2,laguerreRSIClass,dominantCycleClass,parabolicClass,\
    linearRegression,keltnerChannels,choppyMarketFunc
from portfolio import *
from systemAnalytics import *
from utilityFunctions import *
from portManager import *
from positionMatrixClass import *
from barCountCalc import *
from sectorClass import sectorClass, parseSectors, numPosCurrentSector,getCurrentSector, \
    defineSectorUniverse
from tradeProcessing import *
from sysMarkDictionary import * '''


includeCode_A ='''marketMonitorList,masterDateList,masterDateGlob,entryPrice = ([] for i in range(4))
buy = entry = 1; sell = exit = -1; ignore = 0;
entryQuant,exitQuant,trueRanges,myBPVList = ([] for i in range(4))
myComNameList,myComLongNameList,myMinMoveList,systemMarketList = ([] for i in range(4))
marketVal1,marketVal2,marketVal3,marketVal4 = ([] for i in range(4))
cond1,cond2,cond3,cond4 = ([] for i in range(4))
marketVal1List,marketVal2List,marketVal3List,marketVal4List = ([] for i in range(4))
adxList,stochasticList,LagRSIList,parabolicList,rsiList,macdList,domCycleList = \
([] for i in range(7))
portManager = portManagerClass();portfolio = portfolioClass()
sysMarkDict = dict();cumuProfit = 0
numMarkets = len(marketList);positionMatrix = positionMatrixClass();positionMatrix.numMarkets = numMarkets
firstMarketLoop = True; dailyPortCombEqu = portEquItm = barsSinceEntry = curShares = 0
myOHLCTR = list()'''
includeCode_B = '''
for curMarket in range(0,numMarkets):
    systemMarkTracker = systemMarkTrackerClass()
    equity = equityClass()
    systemMarkTracker.setSysMarkTrackingData(marketList[curMarket])
    systemMarkTracker.setSysMarkTrackingEquity(equity)
    marketMonitorList.append(systemMarkTracker)
    myBPV,myComName,myComLongName,myMinMove= getDataAtribs(marketMonitorList[curMarket].marketData)
    myBPVList.append(myBPV);myComNameList.append(myComName);myMinMoveList.append(myMinMove)
    myComLongNameList.append(myComLongName)
    marketVal1List.append([]);marketVal2List.append([]);
    marketVal3List.append([]);marketVal4List.append([])
    cond1.append(0);cond2.append(0);cond3.append(0),cond4.append(0)
    marketVal1.append(0);marketVal2.append(0);marketVal3.append(0),marketVal4.append(0)
    masterDateGlob += marketMonitorList[curMarket].marketData.date
    positionMatrix.marketNames.append(myComNameList[curMarket])
masterDateList = removeDuplicates(masterDateGlob);masterDateList = sorted(masterDateList)'''

includeCode_C = '''
barCount, endBarCount = barCountCalc(masterDateList,startTestDate,stopTestDate,rampUp)
portEquItm = barsSinceEntry = 0;dailyPortCombEqu = initCapital
portOTE = bigOTELoser = bigOTEWinner = bigOTEWinnerNum = bigOTELoserNum = 0
portIndividOTESum = 0
'''


includeCode_D = '''
if curMarket == 0 : indivMktAccum = initCapital
myDate,myOpen,myHigh,myLow,myClose,myVolume,myOpInt,myRange,myTrueRange = setDataLists(marketMonitorList[curMarket].marketData)
myOHLCTR.clear()
myOHLCTR.append(myOpen);myOHLCTR.append(myHigh);myOHLCTR.append(myLow);
myOHLCTR.append(myClose);myOHLCTR.append(myTrueRange)
equItm = marketMonitorList[curMarket].equItm;equItm += 1
myBPV = myBPVList[curMarket];myComName = myComNameList[curMarket];myMinMove = myMinMoveList[curMarket]
mySymbol = myComName
if curMarket == 0 : sectorTradesTodayList = [0] * numSectors
if myComName not in portManager.marketSymbols:
    portManager.marketSymbols.append(myComName)
    portManager.numConts.append(1)
curShares = 0
todaysCTE = todaysOTE = 0
mktsToday = 0'''

includeCode_E = '''
mp = 0;curBar = marketMonitorList[curMarket].marketData.date.index(masterDateList[curPortBar])
if sectorList !=([]):
    numSectorPositions = numPosCurrentSector(sectorList,myComName,myComNameList,positionMatrix.posMatrixSize[-numMarkets:])
    #numSectorPositions = 0
    curSector = getCurrentSector(myComName,sectorList)
else: curSector = 999
if len(marketMonitorList[curMarket].mp)!=0: mp = marketMonitorList[curMarket].mp[-1]
entryPrice,entryQuant,curShares,cumuProfit,barsSinceEntry,barsSinceExit = \
marketMonitorList[curMarket].getSysMarkTrackingInfo()
setSysMarkDict(sysMarkDict,todaysCTE,barsSinceEntry,barsSinceExit,curShares, \
mp,marketMonitorList[curMarket],curMarket,myDate, \
entryPrice,entryQuant,curBar,cumuProfit,myBPV,commission,sectorTradesTodayList,curSector)
D = curBar;D1 = curBar-1;D2 = curBar-2;D3 = curBar-3;D4 = curBar-4;D5 = curBar-5
D6 = curBar-6;D7 = curBar-7;D8 = curBar-8;D9 = curBar-9;D10 = curBar-10'''


includeCode_Last1 = '''
if mp != 0:
    barsSinceEntry += 1
if mp == 0: barsSinceExit +=1
todaysOTE = calcTodaysOTE(mp,marketList[curMarket].close[curBar],marketMonitorList[curMarket].entryPrice,marketMonitorList[curMarket].entryQuant,myBPV)
marketMonitorList[curMarket].setSysMarkTrackingInfoB(barsSinceEntry,barsSinceExit,curShares,equItm,todaysOTE)
marketMonitorList[curMarket].equity.setEquityInfo(marketList[curMarket].date[curBar],equItm,todaysCTE,todaysOTE)
portManager.individEquity.append((curMarket,marketMonitorList[curMarket].equity.dailyEquityVal[-1]))
indivMktAccum += portManager.individEquity[portEquItm][1]
portEquItm += 1
if curPortBar == endBarCount:
    if mp >= 1:
        price = marketList[curMarket].close[curBar]
        exitPosition(price, curShares, "Lx-EOFData",sysMarkDict)
        unPackDict(sysMarkDict)
    if mp <= -1:
        price = marketList[curMarket].close[curBar]
        exitPosition(price, curShares, "Sx-EOFData",sysMarkDict)
        unPackDict(sysMarkDict)'''

includeCode_Last2 = '''
equityStreamLen = len(marketMonitorList[curMarket].equity.dailyEquityVal)
if equityStreamLen > 0: portManager.individEquity.append((curMarket,marketMonitorList[curMarket].equity.dailyEquityVal[-1]))
else: portManager.individEquity.append((curMarket,0.0))
indivMktAccum += portManager.individEquity[portEquItm][1]
portEquItm += 1'''

includeCode_Last3 = '''
if curMarket == numMarkets - 1 and firstMarketLoop == True: firstMarketLoop = False
dailyPortCombEqu = indivMktAccum
portManager.combinedEquity.append(dailyPortCombEqu)
positionMatrix.posMatrixDate.append(masterDateList[curPortBar])
for mktCnt in range(0,len(marketMonitorList)):
    positionMatrix.posMatrixSize.append(marketMonitorList[mktCnt].curShares)'''

includeCode_Last4 = '''
for j in range(0,numMarkets):
    systemMarket = systemMarketClass()
    systemMarket.setSysMarkInfo(sysName,myComNameList[j],myComLongNameList[j],marketMonitorList[j].tradesList,marketMonitorList[j].equity,initCapital)
    systemMarketList.append(systemMarket)
#sectors.setSectorsInfo(numSectors,systemMarketList)
positionMatrix.printPositionMatrix(systemMarketList,portManager)
portfolio.setPortfolioInfo("PortfolioTest",systemMarketList)
if sectorList != ([]): parseSectors(sectorList,systemMarketList)
calcSystemResults(systemMarketList)'''


