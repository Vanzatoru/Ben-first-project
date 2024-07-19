from tsnorgupdater import *

#----------------------------------------------------------------------------------
# Set up algo parameters here
#----------------------------------------------------------------------------------
startTestDate = variabletouse #must be in yyyymmdd
stopTestDate  = 99999999 #must be in yyyymmdd
rampUp = 200 # need this minimum of bars to calculate indicators
sysName = 'TF-System#7_1R' #System Name here
initCapital = 500000
commission = 50
#----------------------------------------------------------------------------------
#instantiate class based indicators
useADX           = False
useLaguerre       = False
useParabolic     = False
useStochastic    = False
useRSI           = False
useMACD          = False
useDominantCycle = True


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

longExit = shortExit = 0

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
    #---------------------------------------------------------------------------------
    # Do not change code above
    #---------------------------------------------------------------------------------
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
#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
#  Define Long, Short, ExitLong and ExitShort Levels - mind your indentations
#  Remember every line of code is executed on every day of every market#
#  Make sure you want to do this - if not it can slow down processing
#  Define Long, Short, ExitLong and ExitShort Levels - mind your indentations
#---------------------------------------------------------------------------------------------------
#-----------tab over 3 times or 12 spaces before typing your code
#-----------
            domCycle = domCycleList[curMarket].calcDomCycle(myDate,myHigh,myLow,myClose,curBar,2)
            domCycle = max(domCycle,20)
            buyLevel= highest(myHigh,int(domCycle*1.1),curBar,2)
            shortLevel = lowest(myLow,int(domCycle*1.1),curBar,2)
            midBand = (buyLevel + shortLevel)/2

 #           print(myDate[curBar]," dom cycle ",int(domCycle)," ",buyLevel," ",shortLevel," ",midBand)
            shortExit = midBand
            longExit =  midBand

            if mp == 1:
                tempLongExit = entryPrice[-1] - 1500/myBPV
                longExit = max(longExit,tempLongExit)
            if mp == -1:
                tempShortExit = entryPrice[-1] + 1500/myBPV
                shortExit = min(shortExit,tempShortExit)
            posSize = 1

            longExit = roundToNearestTick(longExit,-1,myMinMove)
            shortExit = roundToNearestTick(shortExit,1,myMinMove)
            posSize = 1

#  Long Entry
#  Okay  Let's put in some logic to create a long position
            if crosses(myClose,buyLevel,1,curBar-1) and mp !=1 :
                price = myOpen[curBar]
                tradeName = "TF_Sys7:B"
                numShares = posSize
                enterLongPosition(price,posSize,tradeName,sysMarkDict)
                unPackDict(sysMarkDict)
#  Long Exit 1
            if mp == 1 and myLow[curBar] <= longExit and barsSinceEntry > 0:
                price = min(myOpen[curBar],longExit)
                tradeName = "Lxit1"
                numShares = curShares
                exitPosition(price, curShares, tradeName, sysMarkDict)
                unPackDict(sysMarkDict)
#  Short Entry
#  Okay  Let's put in some logic to create a short position
            if crosses(myClose,shortLevel,-1,curBar-1) and mp !=-1:
                price = myOpen[curBar]
                tradeName = "TF_Sys7:S";numShares = posSize
                numShares = posSize
                enterShortPosition(price, numShares, tradeName,sysMarkDict)
                unPackDict(sysMarkDict)
#  Short Exit
            if mp == -1 and myHigh[curBar] >= shortExit and barsSinceEntry > 0:
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
