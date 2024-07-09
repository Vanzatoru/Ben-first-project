#----------------------------------------------------------------------------------
# Set up algo parameters here
#----------------------------------------------------------------------------------
startTestDate = 20100101 #must be in yyyymmdd
stopTestDate = 99999999 #must be in yyyymmdd
rampUp = 100 # need this minimum of bars to calculate indicators
sysName = 'Donch-MAX2NSect-Debug' #System Name here
initCapital = 500000
commission = 100
#--------------------------------------------------------------------------------
#   If you want to ignore a bunch of non-eseential stuff then
#      S C R O L L   A L M O S T  H A L F   W A Y  D O W N
#--------------------------------------------------------------------------------
#TradingSimula18.py - programmed by George Pruitt
#Built on the code and ideas from "The Ultimate Algorithmic Tradins System T-Box"
#Code is broken into sections
#Most sections can and should be ignored
#Each trading algorithm must be programmed with this template
#This is the main entry into the platform
#--------------------------------------------------------------------------------
#Import Section - inlcude functions, classes, variables from external modules
#--------------------------------------------------------------------------------
# --- Do  not change below here
from getData import *
from equityDataClass import *
from tradeClass import *
from systemMarket import *
from indicators import highest,lowest,rsiClass,stochClass,sAverage,bollingerBands,\
    adxClass,sAverage2,laguerreRSIClass,keltnerChannels
from portfolio import *
from systemAnalytics import *
from utilityFunctions import *
from portManager import *
from positionMatrixClass import *
from barCountCalc import *
from sectorClass import parseSectors, numPosCurrentSector,getCurrentSector, \
    defineSectorUniverse
from tradeProcessing import *
from sysMarkDictionary import *
#-------------------------------------------------------------------------------------------------
# Pay no attention to these two functions - unless you want to
#-------------------------------------------------------------------------------------------------
def unPackDict(aDict):
    global mp, todaysCTE,curShares,cumuProfit,barsSinceEntry,barsSinceExit,entryPrice,entryQuant,\
    sectorTradesTodayList,curSector
    mp = aDict.get("mp")
    todaysCTE = aDict.get("todaysCTE")
    curShares = aDict.get("curShares")
    cumuProfit = aDict.get("cumuProfit")
    barsSinceEntry = aDict.get("barsSinceEntry")
    barsSinceExit = aDict.get("barsSinceExit")
    entryPrice = aDict.get("entryPrice")
    entryQuant = aDict.get("entryQuant")
 #   sectorTradesTodayList[curSector] = aDict.get("sectorTradesToday")
 #   marketMonitorList[curMarket] = aDict.get("marketMonitorList")

#-------------------------------------------------------------------------------------------------
marketList = getData(isStock=False) # loads data from .csv or .por file and sets attributes
#-------------------------------------------------------------------------------------------------

#-----initialize first set of internals  here  -- I G N O R E
marketMonitorList,masterDateList,masterDateGlob,entryPrice = ([] for i in range(4))
buy = entry = 1; sell = exit = -1; ignore = 0;
entryQuant,exitQuant,trueRanges,myBPVList = ([] for i in range(4))
myComNameList,myComLongNameList,myMinMoveList,systemMarketList = ([] for i in range(4))
marketVal1,marketVal2,marketVal3,marketVal4 = ([] for i in range(4))
cond1,cond2,cond3,cond4 = ([] for i in range(4))
marketList1,marketList2,marketList3,marketList4 = ([] for i in range(4))
portManager = portManagerClass();portfolio = portfolioClass()
sysMarkDict = dict();cumuProfit = 0
#------completed initializing set of first internals -- I G N O R E

numMarkets = len(marketList);positionMatrix = positionMatrixClass();positionMatrix.numMarkets = numMarkets
firstMarketLoop = True; dailyPortCombEqu = portEquItm = barsSinceEntry = barsSinceExit = curShares = 0


#---------------------------------------------------------------------------------
# Do not change code below
#---------------------------------------------------------------------------------
for curMarket in range(0,numMarkets):
    systemMarkTracker = systemMarkTrackerClass()
    equity = equityClass()
    systemMarkTracker.setSysMarkTrackingData(marketList[curMarket])
    systemMarkTracker.setSysMarkTrackingEquity(equity)
    marketMonitorList.append(systemMarkTracker)
    myBPV,myComName,myComLongName,myMinMove= getDataAtribs(marketMonitorList[curMarket].marketData)
    myBPVList.append(myBPV);myComNameList.append(myComName);myMinMoveList.append(myMinMove)
    myComLongNameList.append(myComLongName)
    marketList1.append([]);marketList2.append([]);
    marketList3.append([]);marketList4.append([])
    cond1.append(False);cond2.append(False);cond3.append(False),cond4.append(False)
    marketVal1.append(0);marketVal2.append(0);marketVal3.append(0),marketVal4.append(0)
    masterDateGlob += marketMonitorList[curMarket].marketData.date
    positionMatrix.marketNames.append(myComNameList[curMarket])
masterDateList = removeDuplicates(masterDateGlob);masterDateList = sorted(masterDateList)
#---------------------------------------------------------------------------------
# Optional - use this area to create user lists and
#            lists of indicator classes - include the list in the loop
#            if you need to instantiate or initialize
#---------------------------------------------------------------------------------

adxList = list()
myOHLCTR = list()
for curMarket in range(0,numMarkets):
    adxList.append(adxClass())


#---------------------------------------------------------------------------------
# Set Up Sectors Here - remember you must use the exact symbol for each marketData
# Review process in book if necessary - predfined for Pinnalce and CSI data
#---------------------------------------------------------------------------------sectorList = list()
sectorList = list()
sectorTradesTodayList = list()
numSectors = 7
defineSectorUniverse(sectorList,"Pinnacle",myComNameList,numSectors)
#defineSectorUniverse(sectorList,"CSI",myComNameList,numSectors)
#---------------------------------------------------------------------------------
# Do not change code below
#---------------------------------------------------------------------------------
barCount, endBarCount = barCountCalc(masterDateList,startTestDate,stopTestDate,rampUp)
portEquItm = barsSinceEntry = 0;dailyPortCombEqu = initCapital


for curPortBar in range(barCount,endBarCount+1):
    portManager.portDate.append(masterDateList[curPortBar])
    if curPortBar % 225 == 0 : print("Working on bar #: ",curPortBar)
    for curMarket in range(0,numMarkets):
        if curMarket == 0 : indivMktAccum = initCapital
        myOHLCTR.clear()
        myDate,myOpen,myHigh,myLow,myClose,myVolume,myOpInt,myRange,myTrueRange = setDataLists(marketMonitorList[curMarket].marketData)
        myOHLCTR.append(myOpen);myOHLCTR.append(myHigh);myOHLCTR.append(myLow);
        myOHLCTR.append(myClose);myOHLCTR.append(myTrueRange)
        equItm = marketMonitorList[curMarket].equItm;equItm += 1
        myBPV = myBPVList[curMarket];myComName = myComNameList[curMarket];myMinMove = myMinMoveList[curMarket]
        if curMarket == 0 : sectorTradesTodayList = [0] * numSectors
        if myComName not in portManager.marketSymbols:
            portManager.marketSymbols.append(myComName)
            portManager.numConts.append(1)
        curShares = 0;todaysCTE = todaysOTE = 0;mktsToday = 0
#---------------------------------------------------------------------------------
# Do not change code above
#---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------
#  Assign lists based on marketMonitor here - assigning temp lists here is great idea
#--------------------------------------------------------------------------------------------------


#---------------------------------------------------------------------------------
# Do not change code below
#---------------------------------------------------------------------------------

        if masterDateList[curPortBar] in marketMonitorList[curMarket].marketData.date:
            mp = 0;curBar = marketMonitorList[curMarket].marketData.date.index(masterDateList[curPortBar])
            if len(marketMonitorList[curMarket].mp)!=0: mp = marketMonitorList[curMarket].mp[-1]
            entryPrice,entryQuant,curShares,cumuProfit,barsSinceEntry,barsSinceExit = \
            marketMonitorList[curMarket].getSysMarkTrackingInfo()
#---Gather Sector Information from Sector Class at start of trading day
            if myDate[curBar] == 20220214:
                xDate = 6
            numSectorPositions = numPosCurrentSector(sectorList,myComName,myComNameList,positionMatrix.posMatrixSize[-numMarkets:])
            curSector = getCurrentSector(myComName,sectorList)
            sectorPositions = numSectorPositions + sectorTradesTodayList[curSector]
#---Now pack everything into the setSysMarkDict - System Market Dictionary
            setSysMarkDict(sysMarkDict,todaysCTE,barsSinceEntry,barsSinceExit,curShares,mp,marketMonitorList[curMarket],curMarket,myDate, \
            entryPrice,entryQuant,curBar,cumuProfit,myBPV,commission,sectorTradesTodayList,curSector)
            D = curBar;D1 = curBar-1;D2 = curBar-2;D3 = curBar-3;D4 = curBar-4;D5 = curBar-5
            D6 = curBar-6;D7 = curBar-7;D8 = curBar-8;D9 = curBar-9;D10 = curBar-10
#---------------------------------------------------------------------------------
# Do not change code above
#---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------
#  Preprocessing prior to the first market of the day is done here
#---------------------------------------------------------------------------------------------------


#---------------------------------------------------------------------------------------------------
#  Start programming your great trading ideas below here - don't touch stuff above
#---------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------
#  Define Long, Short, ExitLong and ExitShort Levels - mind your indentations
#  Remember every line of code is executed on every day of every market#
#  Make sure you want to do this - if not it can slow down processing
#  Define Long, Short, ExitLong and ExitShort Levels - mind your indentations

            buyLevel = highest(myHigh,80,curBar,1)
            shortLevel = lowest(myLow,80,curBar,1)
            longExit = lowest(myLow,20,curBar,1)
            shortExit = highest(myHigh,20,curBar,1)
#            ATR = sAverage(myTrueRange,30,curBar,1)
#            posSize = .005*dailyPortCombEqu/(ATR*myBPV)
#            posSize = int(posSize)
#            posSize = max(posSize,1)
            posSize = 1
#            print(myDate[curBar]," ",myComName," ",mp," ",sectorPositions)
            if mp != 0 : sectorPositions -= 1

#  Long Entry
#  Okay  Let's put in some logic to create a long position
            if myHigh[curBar-1] >= buyLevel and mp !=1 and sectorPositions < 2:
                price = myOpen[curBar]
                tradeName = "Simple Buy"
                numShares = posSize
                enterLongPosition(price,numShares,tradeName,sysMarkDict)
                unPackDict(sysMarkDict)
 # Long Exit
            if mp == 1 and myLow[curBar-1] <= longExit and barsSinceEntry > 1:
                price = myOpen[curBar]
                tradeName = "Lxit"
                numShares = curShares
                exitPosition(price, curShares, tradeName, sysMarkDict)
                unPackDict(sysMarkDict)

#  Short Entry
#  Okay  Let's put in some logic to create a short position
            if myLow[curBar-1] <= shortLevel and mp !=-1 and sectorPositions < 2 :
                price = myOpen[curBar]
                tradeName = "Simple Sell"
                numShares = posSize
                enterShortPosition(price, numShares, tradeName, sysMarkDict)
                unPackDict(sysMarkDict)
#  Short Exit
            if mp == -1 and myHigh[curBar-1] >= shortExit and barsSinceEntry > 1:
                price = myOpen[curBar]
                tradeName = "Sxit"
                numShares = curShares
                exitPosition(price, curShares, tradeName,sysMarkDict)
                unPackDict(sysMarkDict)

#----------------------------------------------------------------------------------------------------------------------------
# - Do not change code below - trade, portfolio accounting - our great idea should stop here
#----------------------------------------------------------------------------------------------------------------------------
            if mp != 0 :barsSinceEntry += 1
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
                    unPackDict(sysMarkDict)
        else:
            equityStreamLen = len(marketMonitorList[curMarket].equity.dailyEquityVal)
            if equityStreamLen > 0: portManager.individEquity.append((curMarket,marketMonitorList[curMarket].equity.dailyEquityVal[-1]))
            else: portManager.individEquity.append((curMarket,0.0))
            indivMktAccum += portManager.individEquity[portEquItm][1]
            portEquItm += 1
    if curMarket == numMarkets - 1 and firstMarketLoop == True: firstMarketLoop = False
    dailyPortCombEqu = indivMktAccum
    portManager.combinedEquity.append(dailyPortCombEqu)
    positionMatrix.posMatrixDate.append(masterDateList[curPortBar])
    for mktCnt in range(0,len(marketMonitorList)):
        positionMatrix.posMatrixSize.append(marketMonitorList[mktCnt].curShares)
cnt = 0
for j in range(0,numMarkets):
    systemMarket = systemMarketClass()
    systemMarket.setSysMarkInfo(sysName,myComNameList[j],myComLongNameList[j],marketMonitorList[j].tradesList,marketMonitorList[j].equity,initCapital)
    systemMarketList.append(systemMarket)
#sectors.setSectorsInfo(numSectors,systemMarketList)
positionMatrix.printPositionMatrix(systemMarketList,portManager)
portfolio.setPortfolioInfo("PortfolioTest",systemMarketList)
parseSectors(sectorList,systemMarketList)
#plotEquityCurve(portfolio)
calcSystemResults(systemMarketList)
