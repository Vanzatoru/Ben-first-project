##----------------------------------------------------------------------------------
# Set up algo parameters here - TradingSimula19 / 2022 Version
#----------------------------------------------------------------------------------
startTestDate = 20100101 #must be in yyyymmdd
stopTestDate = 99999999 #must be in yyyymmdd
rampUp = 100 # need this minimum of bars to calculate indicators
sysName = 'Boll-10KLimitOTE_1R' #System Name here
initCapital = 500000
commission = 100
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

        if curMarket == 0 :
            if firstMarketLoop == False:
                portOTE,bigOTEWinner,bigOTEWinnerNum,bigOTELoser,bigOTELoserNum = \
                getPortfolioOTE(marketMonitorList,numMarkets)

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
            upBand,dnBand, midBand = bollingerBands(myDate,myClose,80,2,curBar,1)
            buyLevel = roundToNearestTick(upBand,1,myMinMove)
            shortLevel =roundToNearestTick(dnBand,-1,myMinMove)
            longExit = roundToNearestTick(midBand,-1,myMinMove)
            shortExit = roundToNearestTick(midBand,1,myMinMove)

#            ATR = sAverage(myTrueRange,30,curBar,1)

#            posSize = .005*dailyPortCombEqu/(ATR*myBPV)
#           print(myDate[curBar]," ",dailyPortCombEqu," ",.005*dailyPortCombEqu," ",ATR*myBPV)
#            posSize = int(posSize)
#            posSize = max(posSize,1)
            posSize = 1

            if marketVal1[curMarket] == 1 and myLow[curBar] < longExit : marketVal1[curMarket] = 0
            if marketVal2[curMarket] == 1 and myHigh[curBar] > shortExit : marketVal2[curMarket] = 0

#  Long Entry
#  Okay  Let's put in some logic to create a long position
            if myHigh[curBar-1] >= buyLevel and mp !=1 and marketVal1[curMarket] != 1:
                price = myOpen[curBar]
                tradeName = "SimpleBuy"
                numShares = posSize
                enterLongPosition(price,posSize,tradeName,sysMarkDict)
                unPackDict(sysMarkDict)
#  Long Exit 1
            if mp == 1 and myLow[curBar-1] <= longExit and barsSinceEntry > 1:
                price = myOpen[curBar]
                tradeName = "Lxit"
                numShares = curShares
                exitPosition(price, curShares, tradeName, sysMarkDict)
                unPackDict(sysMarkDict)

            if mp == 1 and portOTE > 10000 and bigOTEWinnerNum == curMarket and barsSinceEntry > 1:
                price = myOpen[curBar]
                tradeName = "OTE - Lxit"
                numShares = curShares
                marketVal1[curMarket] = 1
                exitPosition(price, curShares, tradeName, sysMarkDict)
                unPackDict(sysMarkDict)

#  Short Entry
#  Okay  Let's put in some logic to create a short position
            if myLow[curBar-1] <= shortLevel and mp !=-1 and marketVal2[curMarket] != 1 :
                price = myOpen[curBar]
                tradeName = "SimpleSell"
                numShares = posSize
                enterShortPosition(price, numShares, tradeName,sysMarkDict)
                unPackDict(sysMarkDict)
#  Short Exit
            if mp == -1 and myHigh[curBar-1] >= shortExit and barsSinceEntry > 1:
                price = myOpen[curBar]
                tradeName = "Sxit1"
                numShares = curShares
                exitPosition(price, curShares, tradeName,sysMarkDict)
                unPackDict(sysMarkDict)

            if mp == -1 and portOTE > 10000 and bigOTEWinnerNum == curMarket and barsSinceEntry > 1:
                price = myOpen[curBar]
                tradeName = "OTE - Sxit"
                marketVal2[curMarket] = 1
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
