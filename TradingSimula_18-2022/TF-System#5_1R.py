from tsnorgupdater import *

#----------------------------------------------------------------------------------
# Set up algo parameters here
#----------------------------------------------------------------------------------
startTestDate = variabletouse #must be in yyyymmdd
stopTestDate  = 99999999 #must be in yyyymmdd
rampUp = 200 # need this minimum of bars to calculate indicators
sysName = 'TF-System#5_1R' #System Name here
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

longExit2 = shortExit2 = 0;

longExit = shortExit = 0
afLimit = 0.20
afStep = 0.02

AF = marketVal1
buyLevel = marketVal2
shortLevel= marketVal3
stopPrice = marketVal4

tradeHH = marketVal1List
tradeLL = marketVal2List


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
    buyLevel.append(9999999)
    shortLevel.append(0)
    tradeHH[curMarket].append(0)
    tradeHH[curMarket].append(0)
    tradeLL[curMarket].append(0)
    tradeLL[curMarket].append(0)
    AF.append(0.02)
    stopPrice.append(0)

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
#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------

#  Define Long, Short, ExitLong and ExitShort Levels - mind your indentations
#  Remember every line of code is executed on every day of every market#
#  Make sure you want to do this - if not it can slow down processing
#  Define Long, Short, ExitLong and ExitShort Levels - mind your indentations
#---------------------------------------------------------------------------------------------------
            buyLevel,shortLevel,midBand = bollingerBands(myDate,myClose,80,2,curBar,1)
#            print(myComName," ",myDate[curBar]," ",myClose[curBar]," ",buyLevel," ",shortLevel," ",myHigh[curBar] >= buyLevel and mp !=1)
            shortExit = shortExit1 = midBand
            longExit = longExit1 = midBand
            if mp == 1 :
                if barsSinceEntry == 2:
                    stopPrice[curMarket] = myLow[curBar-1] - sAverage(myTrueRange,10,curBar-1,1)* 2
                    AF[curMarket] = afStep
                    tradeHH[curMarket].append(myHigh[curBar-1])
                    tradeHH[curMarket].append(myHigh[curBar-1])
                else:
                    if myHigh[curBar-1] > tradeHH[curMarket][-1]:
                        tradeHH[curMarket].append(myHigh[curBar-1])
                    else:
                        tradeHH[curMarket].append(tradeHH[curMarket][-1])
                    stopPrice[curMarket] = stopPrice[curMarket]+ AF[curMarket] * (tradeHH[curMarket][-1] - stopPrice[curMarket])
                    if tradeHH[curMarket][-1] > tradeHH[curMarket][-2] and AF[curMarket] <afLimit:
                        AF[curMarket] = AF[curMarket] + min(afStep,afLimit- AF[curMarket])
                if stopPrice[curMarket] > myLow[curBar-1]:
                    stopPrice[curMarket] =myLow[curBar-1]

            if mp ==-1 :
                if barsSinceEntry == 2:
                    stopPrice[curMarket] = myHigh[curBar-1] + sAverage(myTrueRange,10,curBar-1,1)* 2
                    AF[curMarket] = afStep
                    tradeLL[curMarket].append(myLow[curBar-1])
                    tradeLL[curMarket].append(myLow[curBar-1])
#                    print(myComName," ",myDate[curBar]," barsSinceEntry = ",barsSinceEntry," ",stopPrice[curMarket]," ",sAverage(myTrueRange,10,curBar-1,1)* 2)
                else:
                    if myLow[curBar-1] < tradeLL[curMarket][-1]:
                        tradeLL[curMarket].append(myLow[curBar-1])
                    else:
                        tradeLL[curMarket].append(tradeLL[curMarket][-1])
                    stopPrice[curMarket] = stopPrice[curMarket]- AF[curMarket] * (stopPrice[curMarket]-tradeLL[curMarket][-1] )
                    if tradeLL[curMarket][-1] < tradeLL[curMarket][-2] and AF[curMarket] <afLimit:
                        AF[curMarket] = AF[curMarket] + min(afStep,afLimit- AF[curMarket])
                if stopPrice[curMarket] < myHigh[curBar-1]:
                    stopPrice[curMarket] =myHigh[curBar-1]
#                print(myComName," ",myDate[curBar]," stopPrice ",stopPrice[curMarket]," ",tradeLL[curMarket][-1]," ",tradeLL[curMarket][-2]," ",AF[curMarket])


#            	Sell ( !( "ParTrLX" ) ) next bar at StopPrice stop;

            posSize = 1

#  Long Entry
#  Okay  Let's put in some logic to create a long position
            if  myHigh[curBar] >= buyLevel and mp !=1 :
                price = max(myOpen[curBar],buyLevel)
                tradeName = "TF_Sys5:B"
                numShares = posSize
                enterLongPosition(price,posSize,tradeName,sysMarkDict)
                unPackDict(sysMarkDict)
#  Long Exit 1
            if mp == 1 and myLow[curBar] <= stopPrice[curMarket] and barsSinceEntry > 1:
                price = min(myOpen[curBar],stopPrice[curMarket])
                tradeName = "Lxit1"
                numShares = curShares
                exitPosition(price, curShares, tradeName, sysMarkDict)
                unPackDict(sysMarkDict)

#  Short Entry
#  Okay  Let's put in some logic to create a short position
            if myLow[curBar] <= shortLevel and mp !=-1:
                price = min(myOpen[curBar],shortLevel)
                tradeName = "TF_Sys5:S"
                numShares = posSize
                enterShortPosition(price, numShares, tradeName,sysMarkDict)
                unPackDict(sysMarkDict)
#  Short Exit
            if mp == -1 and myHigh[curBar] >= stopPrice[curMarket] and barsSinceEntry > 1:
                price = max(myOpen[curBar],stopPrice[curMarket])
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
