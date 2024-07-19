from tsnorgupdater import *

#----------------------------------------------------------------------------------
# Set up algo parameters here
#----------------------------------------------------------------------------------
startTestDate = variabletouse #must be in yyyymmdd
stopTestDate = 99999999 #must be in yyyymmdd
rampUp = 300 # need this minimum of bars to calculate indicators
sysName = 'TF-System#4_1R' #System Name here
initCapital = 100000
commission = 50
#----------------------------------------------------------------------------------
#instantiate class based indicators
useADX           = False
useLaguerre       = False
useParabolic     = True
useStochastic    = False
useRSI           = False
useMACD          = False
useDominantCycle = True

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


buyLevel = list()
shortLevel= list()
for curMarket in range(0,numMarkets):
    buyLevel.append(9999999)
    shortLevel.append(0)
    if useADX == True: adxList.append(adxClass()) # instantiating a list of ADX
    if useLaguerre == True: LagRSI.append(laguerreRSIClass())
    if useParabolic == True: parabolicList.append(parabolicClass())
    if useStochastic == True: stochasticList.append(stochClass())
    if useRSI == True: rsiList.append(rsiClass())
    if useMACD == True: macdList.append(macdClass())
    if useDominantCycle == True: domCycleList.append(dominantCycleClass())


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
#  Define Long, Short, ExitLong and ExitShort Levels - mind your indentations
#  Remember every line of code is executed on every day of every market#
#  Make sure you want to do this - if not it can slow down processing
#  Define Long, Short, ExitLong and ExitShort Levels - mind your indentations
#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
#-----------tab over 3 times or 12 spaces before typing your code
#-----------

            parabCl,parabOp,parabPos,parabTrans = parabolicList[curMarket].calcParabolic(myHigh,myLow,0.02,0.2,curBar,1)
            posSize = 1

#  Long Entry
#  Okay  Let's put in some logic to create a long position
            if  parabPos == -1 and myHigh[curBar] >= parabOp and mp !=1 :
                price = max(myOpen[curBar],parabOp)
                tradeName = "TF_Sys4:B"
                numShares = posSize
                enterLongPosition(price,posSize,tradeName,sysMarkDict)
                unPackDict(sysMarkDict)
#  Long Exit
##            if mp == 1 and myClose[curBar-1] <= longExit and barsSinceEntry > 0:
##                price = myOpen[curBar]
##                tradeName = "Lxit"
##                numShares = curShares
##                exitPosition(price, curShares, tradeName, sysMarkDict)
##                unPackDict(sysMarkDict)
#  Short Entry
#  Okay  Let's put in some logic to create a short position
            if parabPos == 1 and myLow[curBar] <= parabOp and mp !=-1:
                price = min(myOpen[curBar],parabOp)
                tradeName = "TF_Sys4:S"
                numShares = posSize
                enterShortPosition(price, numShares, tradeName,sysMarkDict)
                unPackDict(sysMarkDict)
#  Short Exit
##            if mp == -1 and myClose[curBar-1] >= shortExit and barsSinceEntry > 0:
##                price = myOpen[curBar]
##                tradeName = "Sxit"
##                numShares = curShares
##                exitPosition(price, curShares, tradeName,sysMarkDict)
##                unPackDict(sysMarkDict)
###----------------------------------------------------------------------------------------------------------------------------
# - Do not change code below - trade, portfolio accounting - our great idea should stop here
#----------------------------------------------------------------------------------------------------------------------------
            exec(includeCode_Last1)
        else:
            exec(includeCode_Last2)
    exec(includeCode_Last3)

exec(includeCode_Last4)
