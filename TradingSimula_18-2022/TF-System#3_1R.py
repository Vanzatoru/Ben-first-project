#----------------------------------------------------------------------------------
# Set up algo parameters here
#----------------------------------------------------------------------------------
startTestDate = 20100101 #must be in yyyymmdd
stopTestDate  = 99999999 #must be in yyyymmdd
rampUp = 200 # need this minimum of bars to calculate indicators
sysName = 'TF-System#3_1R' #System Name here
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

adxList = list()
stopTrading = list() # user defined list
symbolSect = list()
curTradesList = list() #user defined list
sectADXAvg = list()
sectADXCnt = list()
buyLevel = list()
shortLevel= list()
for curMarket in range(0,numMarkets):
    adxList.append(adxClass()) # instantiating a list of ADX
    stopTrading.append(False)  # initializing a list to False
    symbolSect.append(0)
    buyLevel.append(9999999)
    shortLevel.append(0)

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
#---------------------------------------------------------------------------------------------------

#  Define Long, Short, ExitLong and ExitShort Levels - mind your indentations
#  Remember every line of code is executed on every day of every market#
#  Make sure you want to do this - if not it can slow down processing
#  Define Long, Short, ExitLong and ExitShort Levels - mind your indentations

            buySetUp = highest(myHigh,130,curBar,2)
            shortSetUp = lowest(myLow,130,curBar,2)
            delta = highest(myHigh,20,curBar,2) - lowest(myLow,20,curBar,2)

            if myHigh[curBar-2] == buySetUp:
                buyLevel[curMarket] = min(myClose[curBar-1] + delta,buyLevel[curMarket])
                shortLevel[curMarket] = max(myClose[curBar-1] - delta,shortLevel[curMarket])
#                print(myDate[curBar]," hh >  130 new buy level ",buyLevel[curMarket]," new short level ",shortLevel[curMarket])
            if myLow[curBar-2] == shortSetUp:
                shortLevel[curMarket] = max(myClose[curBar-1] - delta,shortLevel[curMarket])
                buyLevel[curMarket] = min(myClose[curBar-1] + delta,buyLevel[curMarket])
#                print(myDate[curBar]," ll <  130 new buy level ",buyLevel[curMarket]," new short level ",shortLevel[curMarket]," ",myClose[curBar-1] - delta)

            if mp == 1:
                longExit = entryPrice[-1] - 5000/myBPV
                longExit = roundToNearestTick(longExit,-1,myMinMove)
            if mp == -1:
                shortExit = entryPrice[-1] + 5000/myBPV
                shortExit = roundToNearestTick(shortExit,1,myMinMove)
            posSize = 1

#  Long Entry
#  Okay  Let's put in some logic to create a long position
            if buyLevel[curMarket] != 9999999 and myHigh[curBar] >= buyLevel[curMarket] and mp !=1 :
                price = myClose[curBar]
                tradeName = "TF_Sys3:B"
                numShares = posSize
                enterLongPosition(price,posSize,tradeName,sysMarkDict)
                unPackDict(sysMarkDict)
#  Long Exit 1
            if mp == 1 and myLow[curBar] <= longExit and barsSinceEntry > 1:
                price = min(myOpen[curBar],longExit)
                tradeName = "Lxit1"
                numShares = curShares
                exitPosition(price, curShares, tradeName, sysMarkDict)
                unPackDict(sysMarkDict)

#  Short Entry
#  Okay  Let's put in some logic to create a short position
            if shortLevel[curMarket] != 0 and myLow[curBar] <= shortLevel[curMarket] and mp !=-1:
                price = myClose[curBar]
                tradeName = "TF_Sys3:S"
                numShares = posSize
                enterShortPosition(price, numShares, tradeName,sysMarkDict)
                unPackDict(sysMarkDict)
#  Short Exit
            if mp == -1 and myHigh[curBar] >= shortExit and barsSinceEntry > 1:
                price = max(myOpen[curBar],shortExit)
                tradeName = "Sxit"
                numShares = curShares
                exitPosition(price, curShares, tradeName,sysMarkDict)
                unPackDict(sysMarkDict)

            if myHigh[curBar] >= buyLevel[curMarket]: buyLevel[curMarket] = 9999999
            if myLow[curBar] <= shortLevel[curMarket]: shortLevel[curMarket] = 0


#----------------------------------------------------------------------------------------------------------------------------
# - Do not change code below - trade, portfolio accounting - our great idea should stop here
#----------------------------------------------------------------------------------------------------------------------------
            exec(includeCode_Last1)
        else:
            exec(includeCode_Last2)
    exec(includeCode_Last3)

exec(includeCode_Last4)
