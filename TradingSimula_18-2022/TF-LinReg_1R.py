from tsnorgupdater import *

#----------------------------------------------------------------------------------
# Set up algo parameters here
#----------------------------------------------------------------------------------
startTestDate = variabletouse #must be in yyyymmdd
stopTestDate = 99999999 #must be in yyyymmdd
rampUp = 100 # need this minimum of bars to calculate indicators
sysName = 'TF-LinReg_1R' #System Name here
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

#intiation of lists and variables for testing enging
linRegSlope = list()
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
#---------------------------------------------------------------------------------
sectorList = list()
sectorTradesTodayList = list()
numSectors = 7
defineSectorUniverse(sectorList,"Quandl",myComNameList,numSectors)
#---------------------------------------------------------------------------------
#region Do not change code below
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
        calcPosSize = 1

#---------------------------------------------------------------------------------
#region Do not change code below
#---------------------------------------------------------------------------------
        if masterDateList[curPortBar] in marketMonitorList[curMarket].marketData.date:
            exec(includeCode_E)#endregion
#---------------------------------------------------------------------------------------------------
#  Start programming your great trading ideas below here - don't touch stuff above
#  Define Long, Short, ExitLong and ExitShort Levels - mind your indentations
#----------X----------------------------------------------------------------------------------------
#            predictVal1,slopeVal1 = linearRegression(myDate,myClose,60,1,curBar,1)
#            predictVal2,slopeVal2 = linearRegression(myDate,myClose,60,1,curBar,2)
            predictVal1,slopeVal = linearRegression(myDate,myClose,60,1,curBar,1)
            linRegSlope.append(slopeVal)

            downUp = False
            upDown = False

#            if slopeVal1 > 0 and slopeVal2 < 0 : downUp = True
#            if slopeVal1 < 0 and slopeVal2 > 0 : upDown = True
            if firstMarketLoop == False:
                if slopeVal > 0 and marketVal1[curMarket] < 0: downUp = True
                if slopeVal < 0 and marketVal1[curMarket] > 0: upDown = True
            marketVal1[curMarket] =slopeVal

            ATR = sAverage(myTrueRange,30,curBar,1)
            shortExit = longExit = 0
            if mp == 1: longExit   = roundToNearestTick(entryPrice[-1] - 3*ATR,-1,myMinMove)
            if mp ==-1: shortExit  = roundToNearestTick(entryPrice[-1] + 3*ATR,1,myMinMove)
            sum1 = sum2 = 0
            posSize = 1
#  Long Entry
#  Okay  Let's put in some logic to create a long position
            if downUp == True \
            and ATR*myBPV < 1000 and mp !=1:
                price = myOpen[curBar]
                tradeName = "TF-Linear-B"
                numShares = posSize
                enterLongPosition(price, posSize, tradeName,sysMarkDict)
                unPackDict(sysMarkDict)

            if mp == 1 and myLow[curBar] <= longExit and barsSinceEntry > 1:
                price = min(myOpen[curBar],longExit)
                tradeName = "Lxit"
                numShares = curShares
                exitPosition(price, curShares, tradeName, sysMarkDict)
                unPackDict(sysMarkDict)

#  Short Entry
#  Okay  Let's put in some logic to create a short position
            if upDown == True \
            and ATR*myBPV and mp !=-1:
                price = myOpen[curBar]
                tradeName = "TF-Linear-S"
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

#----------------------------------------------------------------------------------------------------------------------------
#region - Do not change code below - trade, portfolio accounting - our great idea should stop here
#----------------------------------------------------------------------------------------------------------------------------
            exec(includeCode_Last1)
        else:
            exec(includeCode_Last2)
    exec(includeCode_Last3)

exec(includeCode_Last4)
#endregion