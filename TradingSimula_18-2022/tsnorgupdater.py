import norgatedata
import pandas as pd

variabletouse = 20000101


def SendNorgData(symb, destination):
    pricedata_dataframe = norgatedata.price_timeseries(symbol=symb,
    stock_price_adjustment_setting = norgatedata.StockPriceAdjustmentType.TOTALRETURN ,
    padding_setting = norgatedata.PaddingType.NONE,
    start_date = pd.Timestamp('1900-01-01'),
    timeseriesformat='pandas-dataframe')

    pricedata_dataframe.reset_index(inplace=True)
    pricedata_dataframe.drop(['Delivery Month', 'Open Interest'], axis=1, inplace=True)
    pricedata_dataframe['Date'] = pricedata_dataframe['Date'].dt.strftime(r'%Y%m%d')
    pricedata_dataframe.to_csv(destination, header= False, index=False)