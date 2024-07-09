##----------------------------------------------------------------------------------
# Set up algo parameters here - TradingSimula19 / 2022 Version
#----------------------------------------------------------------------------------
startTestDate = 20100101 #must be in yyyymmdd
stopTestDate = 99999999 #must be in yyyymmdd
rampUp = 100 # need this minimum of bars to calculate indicators
sysName = 'TF-BollPdigm' #System Name here
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

longExit2 = shortExit2 = 0;

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
            adx,adxR,dmi = adxList[curMarket].calcADX(myHigh,myLow,myClose,20,curBar,1)

            longEntryName = ""
            shortEntryName = ""

            if mp == 1: longEntryName = curTradesList[-1].tradeName
            if mp ==-1: shortEntryName = curTradesList[-1].tradeName

            upBand,dnBand, midBand = bollingerBands(myDate,myClose,80,2,curBar,1)
            upBand2,dnBand2,midBand2 = bollingerBands(myDate,myClose,10,1,curBar,1)

#            print(myDate[curBar-1]," adx : ",adx," ",upBand," ",myClose[curBar-1])

            buyLevel1 = roundToNearestTick(upBand,1,myMinMove)
            shortLevel1 =roundToNearestTick(dnBand,-1,myMinMove)

            longExit1 = roundToNearestTick(midBand,-1,myMinMove)
            shortExit1 = roundToNearestTick(midBand,1,myMinMove)

            ATR = sAverage(myTrueRange,30,curBar,1)

            CMI = choppyMarketFunc(myHigh,myLow,myClose,30,curBar,1)

            buyLevel2 = roundToNearestTick(dnBand2,-1,myMinMove)
            shortLevel2 =roundToNearestTick(upBand2,+1,myMinMove)

            if mp == 1:
                longExit2 = entryPrice[-1]-3*ATR
                longExit2 = roundToNearestTick(longExit2,-1,myMinMove)
                longProf2 = shortLevel2
                marketVal1[curMarket] = longExit2

            if mp == -1:
                shortExit2 = entryPrice[-1]+3*ATR
                shortExit2 = roundToNearestTick(shortExit2,1,myMinMove)
                shortProf2 = buyLevel2
                marketVal2[curMarket] = shortExit2

            posSize = .005*dailyPortCombEqu/(ATR*myBPV)
 #           print(myDate[curBar]," ",dailyPortCombEqu," ",.005*dailyPortCombEqu," ",ATR*myBPV)
            posSize = int(posSize)
            posSize = max(posSize,1)
            posSize = 1
#  Long Entry
#  Okay  Let's put in some logic to create a long position
            if adx < 15 and myLow[curBar] < buyLevel2 and myClose[curBar-1] >= buyLevel2 and mp !=1:
                if mp == 0 or (mp == -1 and barsSinceEntry > 1):
                    tradeName = "L-Sys2"
                    price = min(myOpen[curBar],buyLevel2)
                    numShares = posSize
                    enterLongPosition(price,posSize,tradeName,sysMarkDict)
                    unPackDict(sysMarkDict)

            if adx >= 15 and myClose[curBar-1] >= buyLevel1 and mp !=1:
                price = myOpen[curBar]
                tradeName = "L-Sys1"
                numShares = posSize
                enterLongPosition(price,posSize,tradeName,sysMarkDict)
                unPackDict(sysMarkDict)


#  Long Exit 1
            if longEntryName == "L-Sys1" and mp == 1 and myClose[curBar-1] <= longExit1 and barsSinceEntry > 1:
                price = myOpen[curBar]
                tradeName = "Lxit1"
                numShares = curShares
                exitPosition(price, curShares, tradeName, sysMarkDict)
                unPackDict(sysMarkDict)

            if longEntryName == "L-Sys2" and mp == 1 and myLow[curBar] <= longExit2 and barsSinceEntry > 1:
                price =min(myOpen[curBar],longExit2)
                tradeName = "Lxit2"
                numShares = curShares
                exitPosition(price, curShares, tradeName, sysMarkDict)
                unPackDict(sysMarkDict)

            if longEntryName == "L-Sys2" and adx >=15 and \
                mp == 1 and myHigh[curBar] > longProf2 and barsSinceEntry > 1:
                price =max(myOpen[curBar],longProf2)
                tradeName = "Lxit3"
                numShares = curShares
                exitPosition(price, curShares, tradeName, sysMarkDict)
                unPackDict(sysMarkDict)


#  Short Entry
#  Okay  Let's put in some logic to create a short position
            if adx < 15 and myHigh[curBar] > shortLevel2 and myClose[curBar-1] <= shortLevel2 and mp !=-1 :
                if mp ==0 or (mp == 1 and barsSinceEntry > 1):
                    price = max(myOpen[curBar],shortLevel2)
                    tradeName = "S-Sys2"
                    numShares = posSize
                    enterShortPosition(price, numShares, tradeName,sysMarkDict)
                    unPackDict(sysMarkDict)

            if adx >= 15 and myClose[curBar-1] <= shortLevel1 and mp !=-1 :
                price = myOpen[curBar]
                tradeName = "S-Sys1"
                numShares = posSize
                enterShortPosition(price, numShares, tradeName,sysMarkDict)
                unPackDict(sysMarkDict)

#  Short Exit
            if shortEntryName == "S-Sys1" and mp == -1 and myClose[curBar-1] >= shortExit1 and barsSinceEntry > 1:
                price = myOpen[curBar]
                tradeName = "Sxit1"
                numShares = curShares
                exitPosition(price, curShares, tradeName,sysMarkDict)
                unPackDict(sysMarkDict)

            if shortEntryName == "S-Sys2" and mp == -1 and myHigh[curBar] >= shortExit2 and barsSinceEntry > 1:
                price = max(myOpen[curBar],shortExit2)
                tradeName = "Sxit2"
                numShares = curShares
                exitPosition(price, curShares, tradeName,sysMarkDict)
                unPackDict(sysMarkDict)

            if shortEntryName == "S-Sys2" and adx >= 15 and \
                mp == -1 and myLow[curBar] < shortProf2 and barsSinceEntry > 1:
                price = min(myOpen[curBar],shortProf2)
                tradeName = "Sxit3"
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
