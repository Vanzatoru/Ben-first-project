#----------------------------------------------------------------------------------
# Set up algo parameters here
#----------------------------------------------------------------------------------
startTestDate = 20100101 #must be in yyyymmdd
stopTestDate  = 99999999 #must be in yyyymmdd
rampUp = 200 # need this minimum of bars to calculate indicators
sysName = 'TF-Covel_1R' #System Name here
initCapital = 1000000
commission = 0
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
    if useADX == True: adxList.append(adxClass()) # instantiating a list of ADX
    if useLaguerre == True: LagRSI.append(laguerreRSIClass())
    if useParabolic == True: parabolicList.append(parabolicClass())
    if useStochastic == True: stochasticList.append(stochClass())
    if useRSI == True: rsiList.append(rsiClass())
    if useMACD == True: macdList.append(macdClass())
    if useDominantCycle == True: domCycleList.append(dominantCycleClass())
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

#  Define Long, Short, ExitLong and ExitShort Levels - mind your indentations
            buyLevel   = highest(myHigh,89,curBar,1) + myMinMove
            shortLevel = lowest(myLow,89,curBar,1)   - myMinMove
            longExit   = lowest(myLow,13,curBar,1)   - myMinMove
            shortExit  = highest(myHigh,13,curBar,1) + myMinMove
#            if isNewMonth(myDate,curBar) and curMarket == 0:
#                print(myDate[curBar]," ",dailyPortCombEqu)

# Covel defined the money management rules as:
            ATR = sAverage(myTrueRange,15,curBar,1)
            posSize1 = .02*dailyPortCombEqu/((buyLevel - longExit)*myBPV)
            posSize2 = .02*dailyPortCombEqu/((shortExit - shortLevel)*myBPV)
            posSizeATR = .02*dailyPortCombEqu/(2*ATR*myBPV)

            posSize1 = min(posSize1,posSizeATR)
            posSize2 = min(posSize2,posSizeATR)
            posSize1 = int(posSize1)
            posSize2 = int(posSize2)
            posSize1 = max(posSize1,1)
            posSize2 = max(posSize2,1)
 # if you want to use the money namagement rules comment out the next line
            posSize1 = posSize2 = 1

#  Long Entry
#  Okay  Let's put in some logic to create a long position
            if myHigh[curBar] >= buyLevel and mp !=1:
                price = max(myOpen[curBar],buyLevel)
                tradeName = "TF-Covel-B"
                posSize = posSize1
                enterLongPosition(price,posSize,tradeName,sysMarkDict)
                unPackDict(sysMarkDict)
#  Long Exit 1
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
                tradeName = "TF-Covel-S";
                posSize = posSize2
                enterShortPosition(price, posSize, tradeName,sysMarkDict)
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

