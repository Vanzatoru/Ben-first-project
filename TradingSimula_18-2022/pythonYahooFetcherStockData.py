from yahoo_historical import Fetcher

#This script uses the yahoo_historical library, which is distributed under the Apache 2.0 license
#code by Andrew Porter
stockList = list()

dateD = list()
openD= list()
highD= list()
lowD=list()
closeD=list()
closeAdjD=list()
volumeD=list()

inputFileName = 'Nasdaq100.txt'
target2=open(inputFileName,"r")
for line in target2:
    stockList.append(line.strip()) # note, coma erases the "cartridge return"
target2.close()
for x in range(0,len(stockList)):
    dataList = list()
    dateD.clear()
    openD.clear()
    highD.clear()
    lowD.clear()
    closeD.clear()
    closeAdjD.clear()
    volumeD.clear()
    data = Fetcher(stockList[x], [2010,1,1], [2022,3,31])
    dataList = data.get_historical()
    dateD = list(dataList['Date'])
    openD = list(dataList['Open'])
    highD = list(dataList['High'])
    lowD = list(dataList['Low'])
    closeD = list(dataList['Close'])
    closeAdjD = list(dataList['Adj Close'])
    volumeD = list(dataList['Volume'])
    fileName1 = stockList[x] + '.csv'
    target1 = open(fileName1,"w")
    for days in range(0,len(dateD)):
        outPutLine = str(dateD[days])+','+str(openD[days])+','+str(highD[days])+','+str(lowD[days])+','+str(closeD[days])+','+str(closeAdjD[days])+','+str(volumeD[days])+'\n'
        target1.write(outPutLine)
    target1.close()


print(dataList)
#            Date       Open       High  ...      Close  Adj Close      Volume