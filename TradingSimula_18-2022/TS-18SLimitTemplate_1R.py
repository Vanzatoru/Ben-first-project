#----------------------------------------------------------------------------------
# Set up algo parameters here - TradingSimula19 / 2022 Version
#----------------------------------------------------------------------------------

# simple system to demonstrate entry on a limit based on mean reversion
# with a max loss of $5000

startTestDate = 20100101 #must be in yyyymmdd
stopTestDate = 99999999 #must be in yyyymmdd
rampUp = 200 # need this minimum of bars to calculate indicators
sysName = 'TS-18LimitExample' #System Name here
initCapital = 100000
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
marketList = getData(isStock=False) # loads data from .csv or .por file and sets attributes
#-------------------------------------------------------------------------------------------------

exec(includeCode_A)
exec(includeCode_B)

#---------------------------------------------------------------------------------
# Optional - use this area to create user lists and
#            lists of indicator classes - include the list in the loop
#            if you need to instantiate or initialize
#---------------------------------------------------------------------------------

longExit = shortExit = 0;

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
            myADX,myADXR,myDMI = adxList[curMarket].calcADX(myHigh,myLow,myClose,14,curBar,1)

            movAvg200 = sAverage(myClose,200,D,1)

            if mp == 1:
                longExit = entryPrice[-1] - 5000/myBPV
            if mp == -1:
                 shortExit = entryPrice[-1] + 5000/myBPV
            longExit = roundToNearestTick(longExit,-1,myMinMove)
            shortExit = roundToNearestTick(shortExit,1,myMinMove)
            posSize = 1

#  Long Entry - trade in direction of 200 day moving average
#  After two down closes then enter long on yesterday's low with
#  a limit order
#-------------------------------------------------------------------
#  Okay  Let's put in some logic to create a long position
            if mp < 1 and myClose[D1] > movAvg200 and myClose[D1] < myClose[D2] and \
            myClose[D2] < myClose[D3] and myLow[D] < myLow[D1]:
                price = min(myOpen[D],myLow[D1])
                tradeName = "TS-18-B:Limit"
                numShares = posSize
                enterLongPosition(price,posSize,tradeName,sysMarkDict)
                unPackDict(sysMarkDict)
#  Long Exit 1
            if mp == 1 and myLow[D] <= longExit and barsSinceEntry > 1:
                price = min(myOpen[D],longExit)
                tradeName = "Lxit"
                numShares = curShares
                exitPosition(price, curShares, tradeName, sysMarkDict)
                unPackDict(sysMarkDict)

            if mp == 1 and barsSinceEntry > 1 and myClose[D1] > myClose[D2] and \
            myClose[D1] > entryPrice[-1]:
                price = myOpen[D]
                tradeName = "2B-LProf"
                numShares = curShares
                exitPosition(price, curShares, tradeName, sysMarkDict)
                unPackDict(sysMarkDict)

            if mp == 1 and barsSinceEntry > 5 and myLow[D1] < myLow[D3]:
                price = myOpen[D]
                tradeName = "5B-L1<L3-Lx"
                numShares = curShares
                exitPosition(price, curShares, tradeName, sysMarkDict)
                unPackDict(sysMarkDict)

            if mp == 1 and myLow[D] <= longExit and barsSinceEntry > 1:
                price = min(myOpen[D],longExit)
                tradeName = "Lxit"
                numShares = curShares
                exitPosition(price, curShares, tradeName, sysMarkDict)
                unPackDict(sysMarkDict)


#  Short Entry - trade in direction of 200 day moving average
#  After two up closes then enter short at yesterday's high with
#  a limit order
#-------------------------------------------------------------------

#  Okay  Let's put in some logic to create a short position
            if mp > -1 and myClose[D1] < movAvg200 and myClose[D1] > myClose[D2] and \
            myClose[D2] > myClose[D3] and myHigh[D] > myHigh[D1]:
                price = max(myOpen[D],myHigh[D1])
                tradeName = "TS-18-S:Limit"
                numShares = posSize
                enterShortPosition(price, numShares, tradeName,sysMarkDict)
                unPackDict(sysMarkDict)
#  Short Exit
            if mp == -1 and myHigh[D] >= shortExit and barsSinceEntry > 1:
                price = max(myOpen[D],shortExit)
                tradeName = "Sxit1"
                numShares = curShares
                exitPosition(price, curShares, tradeName,sysMarkDict)
                unPackDict(sysMarkDict)

            if mp == -1 and barsSinceEntry > 1 and myClose[D1] < myClose[D2] and \
            myClose[D1] < entryPrice[-1]:
                price =myOpen[D]
                tradeName = "2B-SProf"
                numShares = curShares
                exitPosition(price, curShares, tradeName,sysMarkDict)
                unPackDict(sysMarkDict)


            if mp == -1 and barsSinceEntry > 5 and myHigh[D1] > myHigh[D3]:
                price = myOpen[D]
                tradeName = "5B-H1>H3-Sx"
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
