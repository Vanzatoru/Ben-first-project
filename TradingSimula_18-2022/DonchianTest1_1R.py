#----------------------------------------------------------------------------------
# TradingSimula_18 Version 1R - refactored in 2021 and 2022
# Much cleaner interface
# Set up algo parameters here
#----------------------------------------------------------------------------------
startTestDate = 20100101 #must be in yyyymmdd
stopTestDate = 99999999 #must be in yyyymmdd
rampUp = 100 # need this minimum of bars to calculate indicators
sysName = 'Donch-Test-1R' #System Name here
initCapital = 100000
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
#---------------------------------------------------------------------------------sectorList = list()
sectorList = list()
sectorTradesTodayList = list()
numSectors = 7
defineSectorUniverse(sectorList,"Quandl",myComNameList,numSectors)
#defineSectorUniverse(sectorList,"CSI",myComNameList,numSectors)
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
#  Assign lists based on marketMonitor here - assigning temp lists here is great idea
#--------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
# Do not change code below
#---------------------------------------------------------------------------------
        if masterDateList[curPortBar] in marketMonitorList[curMarket].marketData.date:
            exec(includeCode_E)

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

#  Long Entry
#  Okay  Let's put in some logic to create a long position
            if myHigh[curBar] >= buyLevel and mp !=1:
                price = max(myOpen[curBar],buyLevel)
                tradeName = "Simple Buy"
                numShares = posSize
                enterLongPosition(price,numShares,tradeName,sysMarkDict)
                unPackDict(sysMarkDict)
 # Long Exit
            if mp == 1 and myLow[curBar] <= longExit and barsSinceEntry > 1:
                price = min(myOpen[curBar],longExit)
                tradeName = "Lxit"
                numShares = curShares
                exitPosition(price, curShares, tradeName, sysMarkDict)
                unPackDict(sysMarkDict)

#  Short Entry
#  Okay  Let's put in some logic to create a short position
            if myLow[curBar] <= shortLevel and mp !=-1:
                price = min(myOpen[curBar],shortLevel)
                tradeName = "Simple Sell"
                numShares = posSize
                enterShortPosition(price, numShares, tradeName, sysMarkDict)
                unPackDict(sysMarkDict)
#  Short Exit
            if mp == -1 and myHigh[curBar] >= shortExit and barsSinceEntry > 1:
                price = max(myOpen[curBar],shortExit)
                tradeName = "Sxit"
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
