from tsnorgupdater import *

#----------------------------------------------------------------------------------
# Set up algo parameters here
#----------------------------------------------------------------------------------
startTestDate = variabletouse #must be in yyyymmdd
stopTestDate = 99999999 #must be in yyyymmdd
rampUp = 300 # need this minimum of bars to calculate indicators
sysName = 'TF-System#1_1R' #System Name here
initCapital = 500000
commission = 50
#----------------------------------------------------------------------------------
#instantiate class based indicators
useADX           = False  # built-in
useLaguerre       = False  # built-in
useParabolic     = False  # built-in
useStochastic    = False  # built-in
useRSI           = False  # built-in
useMACD          = False  # built-in
useDominantCycle = False  # built-in

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

longExit2 = shortExit2 = 0;

stopTrading = list() # user defined list
symbolSect = list()
curTradesList = list() #user defined list
sectADXAvg = list()
sectADXCnt = list()
for curMarket in range(0,numMarkets):
    if useADX == True: adxList.append(adxClass()) # instantiating a list of ADX
    if useLaguerre == True: LagRSI.append(laguerreRSIClass())
    if useParabolic == True: parabolicList.append(parabolicClass())
    if useStochastic == True: stochasticList.append(stochClass())
    if useRSI == True: rsiList.append(rsiClass())
    if useMACD == True: macdList.append(macdClass())
    if useDominantCycle == True: domCycleList.append(dominantCycleClass())
    stopTrading.append(False)  # initializing a list to False
    symbolSect.append(0)

#---------------------------------------------------------------------------------
# Set Up Sectors Here - remember you must use the exact symbol for each marketData
# Review process in book if necessary - predfined for Pinnalce and CSI data
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
    #---------------------------------------------------------------------------------
    # Do not change code above
    #---------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------
    #  Assign lists based on marketMonitor here - assigning temp lists here is great idea
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
#---------------------------------------------------------------------------------------------------

#  Define Long, Short, ExitLong and ExitShort Levels - mind your indentations
#  Remember every line of code is executed on every day of every market#
#  Make sure you want to do this - if not it can slow down processing
#  Define Long, Short, ExitLong and ExitShort Levels - mind your indentations

#  Build some weekly bars
            dateW,openW,highW,lowW,closeW,rangeW,tRangeW = getWeeklyData(marketMonitorList[curMarket].marketData,9,curBar)
            weeklyAVGRange = sAverage2(rangeW,8,2)
            dailyATR = sAverage(myTrueRange,20,curBar,1)
            buyLevel = sAverage(myClose,39,curBar,1) + weeklyAVGRange*2
            shortLevel= sAverage(myClose,39,curBar,1) - weeklyAVGRange*2
#            print(myDate[curBar-1]," ",myClose[curBar-1]," ",shortLevel," ",sAverage(myClose,39,curBar,1)," ",weeklyAVGRange)
            shortExit = 999999
            longExit = 0
            if mp == 1 :
                longExit = entryPrice[-1] - 3 *dailyATR
                longExit = max(longExit,entryPrice[-1] - 5000/myBPV)
            if mp ==-1 :
                shortExit = entryPrice[-1] + 3 *dailyATR
                shortExit = min(shortExit,entryPrice[-1]+ 5000/myBPV)
            posSize = 1

#  Long Entry
#  Okay  Let's put in some logic to create a long position
            if crosses(myClose,buyLevel,1,curBar-1) and mp !=1 :
                price = myOpen[curBar]
                tradeName = "TF_Sys1:B"
                numShares = posSize
                enterLongPosition(price,posSize,tradeName,sysMarkDict)
                unPackDict(sysMarkDict)
#  Long Exit
            if mp == 1 and myClose[curBar-1] <= longExit and barsSinceEntry > 0:
                price = myOpen[curBar]
                tradeName = "Lxit"
                numShares = curShares
                exitPosition(price, curShares, tradeName, sysMarkDict)
                unPackDict(sysMarkDict)
#  Short Entry
#  Okay  Let's put in some logic to create a short position
            if crosses(myClose,shortLevel,-1,curBar-1) and mp !=-1:
                price = myOpen[curBar]
                tradeName = "TF_Sys1:S"
                numShares = posSize
                enterShortPosition(price, numShares, tradeName,sysMarkDict)
                unPackDict(sysMarkDict)
#  Short Exit
            if mp == -1 and myClose[curBar-1] >= shortExit and barsSinceEntry > 0:
                price = myOpen[curBar]
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
