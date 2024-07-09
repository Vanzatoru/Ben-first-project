#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      George
#
# Created:     25/01/2021
# Copyright:   (c) George 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def setSysMarkDict(sysMarkDict,todaysCTE,barsSinceEntry,barsSinceExit,curShares,mp,marketMonitor, \
curMarket,myDate,entryPrice,entryQuant,curBar,cumuProfit,myBPV,commission,sectorTradesTodayList, \
curSector):
        sysMarkDict["todaysCTE"] = todaysCTE
        sysMarkDict["barsSinceEntry"] = barsSinceEntry
        sysMarkDict["barsSinceExit"] = barsSinceExit
        sysMarkDict["curShares"] = curShares
        sysMarkDict["mp"] = mp
        sysMarkDict["marketMonitor"] = marketMonitor
        sysMarkDict["curMarket"] = curMarket
        sysMarkDict["myDate"] = myDate
        sysMarkDict["entryPrice"] = entryPrice
        sysMarkDict["entryQuant"] = entryQuant
        sysMarkDict["curBar"] = curBar
        sysMarkDict["cumuProfit"] = cumuProfit
        sysMarkDict["myBPV"] = myBPV
        sysMarkDict["commission"] = commission
        sysMarkDict["sectorTradesTodayList"] = sectorTradesTodayList
        sysMarkDict["curSector"] = curSector
        return(sysMarkDict)
