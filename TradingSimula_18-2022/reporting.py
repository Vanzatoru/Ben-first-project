import quantstats
import pandas as pd
import matplotlib.pyplot as plt
import quantstats._plotting
import imgkit

def qsreport(data):
    df = pd.read_csv(data)
    df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d')
    df.set_index('Date', inplace=True)
    #rep = quantstats.plots.log_returns(data)
    df.rename(columns={df.columns[-1]: "Returns"}, inplace=True)
    columns_to_keep = ['Date', 'Returns']
    df.drop(columns=df.columns.difference(columns_to_keep), inplace=True)
    periodic_returns = df['Returns'].pct_change().dropna()
    #returns = quantstats.plots.log_returns(df, savefig='log_returns_plot', figsize=(8,4))
    #drawdown = quantstats.plots.drawdown(df, savefig='drawdown', figsize=(8,3))
    #dev = quantstats.plots.histogram(df, savefig='Distribution', figsize=(8,3))
    title = data.replace("-PosMatrix.txt","")
    report = quantstats.reports.html(periodic_returns, output="full_report.html", title=title)
    imgkit.from_file("full_report.html", 'out.png')
