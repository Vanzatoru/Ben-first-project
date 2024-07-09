##----------------------------------------------------------------------------------
# Set up algo parameters here - TradingSimula19 / 2022 Version
#----------------------------------------------------------------------------------
startTestDate = 20100101 #must be in yyyymmdd
stopTestDate = 99999999 #must be in yyyymmdd
rampUp = 100 # need this minimum of bars to calculate indicators
sysName = 'TF-ADX-SELECT_1R' #System Name here
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

stopTrading = list()

#Initiate any lists to hold indicator classes here or any other market based lists
for curMarket in range(0,numMarkets):
    if useADX == True: adxList.append(adxClass()) # instantiating a list of ADX
    if useLaguerre == True: LagRSI.append(laguerreRSIClass())
    if useParabolic == True: parabolicList.append(parabolicClass())
    if useStochastic == True: stochasticList.append(stochClass())
    if useRSI == True: rsiList.append(rsiClass())
    if useMACD == True: macdList.append(macdClass())
    if useDominantCycle == True: domCycleList.append(dominantCycleClass())
    # fill up these lists - one for each market in portfolio
    stopTrading.append(False)  # initializing a list to False

#------ initiate algo specific variables here------------------------------------
portfolioClsTrdEqu = portfolioOTEEqu = 0
longExit2 = shortExit2 = 0;
canTrade = True
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

# -- good place to put sector specific lists and variables
# -- prefill sectADXAvg list  with 0's and sectADXCnt list weith negative 1's
sectADXAvg = list()
sectADXCnt = list()

for i in range(0,len(sectorList)):
    sectADXAvg.append(0);sectADXCnt.append(-1)


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
#-------------------------------------------------------------------------------------
#  Preprocessing prior to the first market of the day is done here
#  First market of the day occurs when curMarket == 0
#-------------------------------------------------------------------------------------
            if(isNewMonth(masterDateList,curPortBar) and firstMarketLoop == False and curMarket == 0):
                for numSect in range(0,len(sectorList)):
                    sectADXAvg[numSect] = 0
                    sectADXCnt[numSect] = -1
                for cnt in range(0,numMarkets):
                    tempName = myComNameList[cnt]
                    whichSector = getCurrentSector(tempName,sectorList)
                    if whichSector !=-1:
                        sectADXAvg[whichSector] += marketVal1[cnt]
                        sectADXCnt[whichSector] +=1
                for numSect in range(0,len(sectorList)):
                    if sectADXCnt[numSect] != -1:
                        sectADXAvg[numSect]= sectADXAvg[numSect]/(sectADXCnt[numSect]+1)
                for cnt in range(0,numMarkets):
                    stopTrading[cnt] = False
                    whichSector = getCurrentSector(myComNameList[cnt],sectorList)
                    if  whichSector != -1:
                        if sectADXCnt[whichSector] != -1 :
                            if sectADXAvg[whichSector] < 20:
                                 stopTrading[cnt] = True
#                print(myDate[curBar]," ",marketVal1[0]," ",marketVal1[1]," ",sectADXAvg[0]," ",sectADXCnt[0]," ",stopTrading[0]," ",stopTrading[1])
            marketVal1[curMarket],marketVal2[curMarket],marketVal3[curMarket] = \
            adxList[curMarket].calcADX(myHigh,myLow,myClose,20,curBar,1)

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
#            stopTrading[curMarket] = False

#  Long Entry
#  Okay  Let's put in some logic to create a long position
            if crosses(myClose,buyLevel,1,curBar-1) and mp !=1 and stopTrading[curMarket] == False:
                price = myOpen[curBar]
                tradeName = "TF-Bol-B-Cl"
                numShares = posSize
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
#  Long Exit 2
            if mp == 1 and stopTrading[curMarket] == True:
                price = myOpen[curBar]
                tradeName = "ADXLxit"
 #               if canTrade == False : print("LongExit when canTrade = False")
                numShares = curShares
                exitPosition(price, curShares, tradeName, sysMarkDict)
                unPackDict(sysMarkDict)


#  Short Entry
#  Okay  Let's put in some logic to create a short position
            if crosses(myClose,shortLevel,-1,curBar-1) and mp !=-1 and stopTrading[curMarket] == False:
                price = myOpen[curBar]
                tradeName = "TF-Bol-S-Cl"
                numShares = posSize
                enterShortPosition(price, numShares, tradeName,sysMarkDict)
                unPackDict(sysMarkDict)
#  Short Exit 1
            if mp == -1 and myClose[curBar-1] >= shortExit and barsSinceEntry > 1:
                price = myOpen[curBar]
                tradeName = "Sxit"
                numShares = curShares
                exitPosition(price, curShares, tradeName,sysMarkDict)
                unPackDict(sysMarkDict)
#  Short Exit 2
            if mp == -1 and stopTrading[curMarket] == True:
                price = myOpen[curBar]
                tradeName = "ADXSxit"
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
