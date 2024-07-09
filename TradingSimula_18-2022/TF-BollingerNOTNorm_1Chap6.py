#----------------------------------------------------------------------------------
# Set up algo parameters here
#----------------------------------------------------------------------------------
startTestDate = 20000101 #must be in yyyymmdd
stopTestDate = 99999999 #must be in yyyymmdd
rampUp = 100 # need this minimum of bars to calculate indicators
sysName = 'TF-Boll-Notional' #System Name here
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

from getData import getChildData

exec(includeImports)
exec(includeCodeDict)
#-------------------------------------------------------------------------------------------------
marketList = getData(isStock = False) # loads data from .csv or .por file and sets attributes
#-------------------------------------------------------------------------------------------------

#child data to be use for soybeans
child1Data = getChildData("C:\CLCDATA\ZS_NON.CSV",startTestDate)
child1Index = 0

exec(includeCode_A)
exec(includeCode_B)

#---------------------------------------------------------------------------------
# Optional - use this area to create user lists and
#            lists of indicator classes - include the list in the loop
#            if you need to instantiate or initialize
#---------------------------------------------------------------------------------

maxNotValue = 0
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

#---------------------------------------------------------------------------------
# Set Up Sectors Here - remember you must use the exact symbol for each marketData
# Review process in book if necessary - predfined for Pinnalce and CSI data
# You can make changes in the sectorClass.py module in the defineSectorUniverse
# code
#---------------------------------------------------------------------------------
sectorList = list()
sectorTradesTodayList = list()
numSectors = 7
defineSectorUniverse(sectorList,"Pinnacle",myComNameList,numSectors)
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
#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------

#  Define Long, Short, ExitLong and ExitShort Levels - mind your indentations
#  Remember every line of code is executed on every day of every market#
#  Make sure you want to do this - if not it can slow down processing
#  Define Long, Short, ExitLong and ExitShort Levels - mind your indentations

            myADX,myADXR,myDMI = adxList[curMarket].calcADX(myHigh,myLow,myClose,14,curBar,1)
            if myComName == "ZS":
                for rows in range(child1Index,len(child1Data)):
                    if myDate[curBar] == child1Data[rows][0]:
                        marketVal1[curMarket] = child1Data[rows][4]
                        child1Index = rows
                        break
            else:
                marketVal1[curMarket] = myClose[curBar]
            marketVal2[curMarket] = myBPV

            if firstMarketLoop == False and curMarket == 0:
                maxNotValue = 0
                for mkt in range(0,numMarkets):
                    maxNotValue = max(maxNotValue,marketVal1[mkt]*marketVal2[mkt])
            if firstMarketLoop == False:
                if marketVal1[curMarket] > 0 :
                    posSize = maxNotValue/(marketVal1[curMarket]*myBPV)
                posSize = int(posSize)
                posSize = max(posSize,1)
                posSize = min(posSize,100)
            else:
                posSize = 1


#  Define Long, Short, ExitLong and ExitShort Levels - mind your indentations
            upBand,dnBand, midBand = bollingerBands(myDate,myClose,80,2,curBar,1)
            buyLevel = roundToNearestTick(upBand,1,myMinMove)
            shortLevel =roundToNearestTick(dnBand,-1,myMinMove)
            longExit = roundToNearestTick(midBand,-1,myMinMove)
            shortExit = roundToNearestTick(midBand,1,myMinMove)

            if mp == 1:
                tempLongExit = entryPrice[-1] - 5000/myBPV
                longExit = max(longExit,tempLongExit)
            if mp == -1:
                tempShortExit = entryPrice[-1] + 5000/myBPV
                shortExit = min(shortExit,tempShortExit)


            ATR = sAverage(myTrueRange,30,curBar,1)

#  Long Entry
#  Okay  Let's put in some logic to create a long position
            if myClose[D1] >= buyLevel and mp !=1 :
                price = myOpen[D]
                tradeName = "TF-Bol-B"
                numShares = posSize
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
            if myClose[D1] <= shortLevel and  mp !=-1:
                price = myOpen[D]
                tradeName = "TF-Bol-S"
                numShares = posSize
                enterShortPosition(price, numShares, tradeName,sysMarkDict)
                unPackDict(sysMarkDict)
#  Short Exit
            if mp == -1 and myHigh[curBar] >= shortExit and barsSinceEntry > 1:
                price = max(myOpen[curBar],shortExit)
                tradeName = "Sxit1"
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
