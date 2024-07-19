from tsnorgupdater import *

##----------------------------------------------------------------------------------
# Set up algo parameters here - TradingSimula19 / 2022 Version
#----------------------------------------------------------------------------------
startTestDate = variabletouse #must be in yyyymmdd
stopTestDate = 99999999 #must be in yyyymmdd
rampUp = 100 # need this minimum of bars to calculate indicators
sysName = 'TF-BollwBO' #System Name here
initCapital = 500000
commission = 50
#----------------------------------------------------------------------------------
#instantiate class based indicators
useADX           = True
useLaguerre       = False
useParabolic     = False
useStochastic    = False
useRSI           = False
useMACD          = False
useDominantCycle = False

from IncludeCode import includeImports,includeCodeDict,includeCode_A,includeCode_B
from IncludeCode import includeCode_C,includeCode_D,includeCode_E
from IncludeCode import includeCode_Last1,includeCode_Last2,includeCode_Last3
from IncludeCode import includeCode_Last4

exec(includeImports)
exec(includeCodeDict)
#-------------------------------------------------------------------------------------------------
marketList = getData(isStock = False) # loads data from .csv or .por file and sets attributes
#-------------------------------------------------------------------------------------------------

exec(includeCode_A)
exec(includeCode_B)

#---------------------------------------------------------------------------------
# Optional - use this area to create user lists and
#            lists of indicator classes - include the list in the loop
#            if you need to instantiate or initialize
#---------------------------------------------------------------------------------

longExit2 = shortExit2 = 0;
stopTrading = list() # user defined list
symbolSect = list()
curTradesList = list() #user defined list
sectADXAvg = list()
sectADXCnt = list()

portOTE = bigOTELoser = bigOTEWinner = bigOTEWinnerNum = bigOTELoserNum = 0
portIndividOTESum = 0


#region Initiate any lists to hold indicator classes here
for curMarket in range(0,numMarkets):
    if useADX == True: adxList.append(adxClass()) # instantiating a list of ADX
    if useLaguerre == True: LagRSI.append(laguerreRSIClass())
    if useParabolic == True: parabolicList.append(parabolicClass())
    if useStochastic == True: stochasticList.append(stochClass())
    if useRSI == True: rsiList.append(rsiClass())
    if useMACD == True: macdList.append(macdClass())
    if useDominantCycle == True: domCycleList.append(dominantCycleClass())
#endregion

    stopTrading.append(False)  # initializing a list to False
    symbolSect.append(0)

#---------------------------------------------------------------------------------
# Set Up Sectors Here - remember you must use the exact symbol for each marketData
# Review process in book if necessary - predfined for Pinnalce and CSI data
# You can make changes in the sectorClass.py module in the defineSectorUniverse
# code
#---------------------------------------------------------------------------------
sectorList = list()
sectorTradesTodayList = list()
numSectors = 7
defineSectorUniverse(sectorList,"Quandl",myComNameList,numSectors)
#---------------------------------------------------------------------------------
# Do not change code below
#---------------------------------------------------------------------------------
exec(includeCode_C)
for curPortBar in range(barCount,endBarCount+1):
    portManager.portDate.append(masterDateList[curPortBar])
    if curPortBar % 225 == 0 : print("Working on bar #: ",curPortBar)
    for curMarket in range(0,numMarkets):
        exec(includeCode_D)
    #---------------------------------------------------------------------------------------------------
    #  Assign lists based on marketMonitor here - assigning temp lists here is a great idea
    #--------------------------------------------------------------------------------------------------
        curTradesList = marketMonitorList[curMarket].tradesList
        curMarketData = marketMonitorList[curMarket].marketData

        longEntryName = ""
        shortEntryName = ""

#
    #---------------------------------------------------------------------------------
    # Do not change code below
    #---------------------------------------------------------------------------------
        if masterDateList[curPortBar] in marketMonitorList[curMarket].marketData.date:
            exec(includeCode_E)
#---------------------------------------------------------------------------------------------------
#  Start programming your great trading ideas below here - don't touch stuff above
#  Define Long, Short, ExitLong and ExitShort Levels - mind your indentations
#  Remember every line of code is executed on every day of every market#
#  Make sure you want to do this - if not it can slow down processing
#  Define Long, Short, ExitLong and ExitShort Levels - mind your indentations
#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
#-----------tab over 3 times or 12 spaces before typing your code
#-----------
            if mp == 1: longEntryName = curTradesList[-1].tradeName
            if mp ==-1: shortEntryName = curTradesList[-1].tradeName
            upBand,dnBand, midBand = bollingerBands(myDate,myClose,80,2,curBar,1)

            buyLevel1 = roundToNearestTick(upBand,1,myMinMove)
            shortLevel1 =roundToNearestTick(dnBand,-1,myMinMove)

            longExit1 = roundToNearestTick(midBand,-1,myMinMove)
            shortExit1 = roundToNearestTick(midBand,1,myMinMove)

            ATR = sAverage(myTrueRange,30,curBar,1)

            CMI = choppyMarketFunc(myHigh,myLow,myClose,30,curBar,1)

            buyLevel2 = myClose[curBar-1] + 1 * ATR
            buyLevel2 = roundToNearestTick(buyLevel2,1,myMinMove)

            shortLevel2 = myClose[curBar-1] - 1 * ATR
            shortLevel2 =roundToNearestTick(shortLevel2,-1,myMinMove)

            if mp == 1:
                longExit2 = entryPrice[-1]-3*ATR
                longExit2 = max(longExit2,lowest(myLow,10,curBar,1))
                longExit2 = roundToNearestTick(longExit2,-1,myMinMove)
                marketVal1[curMarket] = longExit2


            if mp == -1:
                shortExit2 = entryPrice[-1]+3*ATR
                shortExit2 = min(shortExit2,highest(myHigh,10,curBar,1))
                shortExit2 = roundToNearestTick(shortExit2,1,myMinMove)
                marketVal2[curMarket] = shortExit2

            posSize = .005*dailyPortCombEqu/(ATR*myBPV)
            posSize = int(posSize)
            posSize = max(posSize,1)
            posSize = 1
#  Long Entry
#  Okay  Let's put in some logic to create a long position
            if CMI < 20 and myHigh[curBar] >= buyLevel2 and myClose[curBar-1] < myClose[curBar-2] and mp !=1:
                tradeName = "TF-BrkO-L"
                price = max(myOpen[curBar],buyLevel2)
                numShares = posSize
                enterLongPosition(price,posSize,tradeName,sysMarkDict)
                unPackDict(sysMarkDict)

            if CMI >= 20 and myClose[curBar-1] >= buyLevel1 and mp !=1:
                price = myOpen[curBar]
                tradeName = "TF-Bol-B-Cl"
                price = myOpen[curBar]
                numShares = posSize
                enterLongPosition(price,posSize,tradeName,sysMarkDict)
                unPackDict(sysMarkDict)

#  Long Exit 1
            if longEntryName == "TF-BOL-B-Cl" and mp == 1 and myClose[curBar-1] <= longExit1 and barsSinceEntry > 1:
                price = myOpen[curBar]
                tradeName = "Lxit1"
                numShares = curShares
                exitPosition(price, curShares, tradeName, sysMarkDict)
                unPackDict(sysMarkDict)

            if longEntryName == "TF-BrkO-L" and mp == 1 and myLow[curBar] <= longExit2 and barsSinceEntry > 1:
                price =min(myOpen[curBar],longExit2)
                tradeName = "Lxit2"
                numShares = curShares
                exitPosition(price, curShares, tradeName, sysMarkDict)
                unPackDict(sysMarkDict)


#  Short Entry
#  Okay  Let's put in some logic to create a short position
            if CMI < 20 and myLow[curBar] <= shortLevel2 and myClose[curBar-1] > myClose[curBar-2] and mp !=-1:
                price = min(myOpen[curBar],shortLevel2)
                tradeName = "TF-BrkO-S"
                numShares = posSize
                enterShortPosition(price, numShares, tradeName,sysMarkDict)
                unPackDict(sysMarkDict)

            if CMI >= 20 and myClose[curBar-1] <= shortLevel1 and mp !=-1:
                price = myOpen[curBar]
                tradeName = "TF-Bol-S-Cl";numShares = posSize
                numShares = posSize
                enterShortPosition(price, numShares, tradeName,sysMarkDict)
                unPackDict(sysMarkDict)

            if shortEntryName == "TF-Bol-S-Cl" and mp == -1 and myClose[curBar-1] >= shortExit1 and barsSinceEntry > 1:
                price = myOpen[curBar]
                tradeName = "Sxit1"
                numShares = curShares
                exitPosition(price, curShares, tradeName,sysMarkDict)
                unPackDict(sysMarkDict)

            if shortEntryName == "TF-BrkO-S" and mp == -1 and myHigh[curBar] >= shortExit2 and barsSinceEntry > 1:
                price = max(myOpen[curBar],shortExit2)
                tradeName = "Sxit2"
                numShares = curShares
                exitPosition(price, curShares, tradeName,sysMarkDict)
                unPackDict(sysMarkDict)


#----------------------------------------------------------------------------------------------------------------------------
# - Do not change code below - trade, portfolio accounting - our great idea should stop here
#----------------------------------------------------------------------------------------------------------------------------
            exec(includeCode_Last1)
        else:
            exec(includeCode_Last2)
    exec(includeCode_Last3)

exec(includeCode_Last4)
