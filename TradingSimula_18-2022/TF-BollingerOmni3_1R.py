##----------------------------------------------------------------------------------
# Set up algo parameters here - TradingSimula19 / 2022 Version
#----------------------------------------------------------------------------------
startTestDate = 20100101 #must be in yyyymmdd
stopTestDate = 99999999 #must be in yyyymmdd
rampUp = 100 # need this minimum of bars to calculate indicators
sysName = 'TF-Boll-Omni3_1R' #System Name here
initCapital = 500000
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

#---------------------------------------------------------------------------------
# Optional - use this area to create user lists and
#            lists of indicator classes - include the list in the loop
#            if you need to instantiate or initialize
#---------------------------------------------------------------------------------

longExit2 = shortExit2 = 0;
canTrade = True


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

        avgLong,avgShort,numLong,numShort = calcAvgLongShort(curTradesList,10)
#
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
            newMonth = isNewMonth(masterDateList,curPortBar)
            if canTrade == True and curMarket == 0:
                portfolioClsTrdEqu = 0
                for tempCurMarket in range(0,numMarkets):
                    portfolioClsTrdEqu += marketMonitorList[tempCurMarket].equity.cumuClsEquity
            if newMonth:
                begOfMonthPortEqu = portfolioClsTrdEqu
            canTrade = True
            if portfolioClsTrdEqu < begOfMonthPortEqu - 5000:
                canTrade = False
                print(myDate[curBar]," stopped trading")

            upBand,dnBand, midBand = bollingerBands(myDate,myClose,80,2,curBar,1)
            buyLevel = roundToNearestTick(upBand,1,myMinMove)
            shortLevel =roundToNearestTick(dnBand,-1,myMinMove)
            longExit = roundToNearestTick(midBand,-1,myMinMove)
            shortExit = roundToNearestTick(midBand,1,myMinMove)

            ATR = sAverage(myTrueRange,30,curBar,1)

#            posSize = .005*dailyPortCombEqu/(ATR*myBPV)
#           print(myDate[curBar]," ",dailyPortCombEqu," ",.005*dailyPortCombEqu," ",ATR*myBPV)
#            posSize = int(posSize)
#            posSize = max(posSize,1)
            posSize = 1


#  Long Entry
#  Okay  Let's put in some logic to create a long position
            if myClose[curBar-1] >= buyLevel and mp !=1 and canTrade:
                price = myOpen[curBar]
                tradeName = "TF-Bol-B-Cl"
                numShares = posSize
                enterLongPosition(price,posSize,tradeName,sysMarkDict)
                unPackDict(sysMarkDict)
#  Long Exit 1
            if mp == 1 and myClose[curBar-1] <= longExit and barsSinceEntry > 1:
                price = myOpen[curBar]
                tradeName = "Lxit"
 #               if canTrade == False : print("LongExit when canTrade = False")
                numShares = curShares
                exitPosition(price, curShares, tradeName, sysMarkDict)
                unPackDict(sysMarkDict)


#  Short Entry
#  Okay  Let's put in some logic to create a short position
            if myClose[curBar-1] <= shortLevel and mp !=-1 and canTrade:
                price = myOpen[curBar]
                tradeName = "TF-Bol-S-Cl"
                numShares = posSize
                enterShortPosition(price, numShares, tradeName,sysMarkDict)
                unPackDict(sysMarkDict)
#  Short Exit
            if mp == -1 and myClose[curBar-1] >= shortExit and barsSinceEntry > 1:
                price = myOpen[curBar]
                tradeName = "Sxit"
#                if canTrade == False : print("Short Exit when canTrade = False")
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
