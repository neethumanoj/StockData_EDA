import pandas_datareader.data as web
import pandas as pd
import numpy as np
import datetime
import seaborn as sns
from matplotlib import pyplot as plt

# We need to get data using pandas datareader. We will get stock information for the following banks:
#
# Bank of America
# CitiGroup
# Goldman Sachs
# JPMorgan Chase
# Morgan Stanley
# Wells Fargo

# Use datetime to set start and end datetime objects.
# Figure out the ticker symbol for each bank.
# Figure out how to use pandas datareader to grab info on the stock.

start = datetime.datetime(2006, 1, 1)
end = datetime.datetime(2016, 1, 1)

df_BAC = web.DataReader('BAC', 'yahoo', start, end)
df_C = web.DataReader('C', 'yahoo', start='2006-01-01', end='2016-01-01')
df_GS = web.DataReader('GS', 'yahoo', start='2006-01-01', end='2016-01-01')
df_JPM = web.DataReader('JPM', 'yahoo', start='2006-01-01', end='2016-01-01')
df_MS = web.DataReader('MS', 'yahoo', start='2006-01-01', end='2016-01-01')
df_WFC = web.DataReader('WFC', 'yahoo', start='2006-01-01', end='2016-01-01')

# Create a list of the ticker symbols (as strings) in alphabetical order. Call this list: tickers
tickers = ['BAC', 'C', 'GS', 'JPM', 'MS', 'WFC']

# Use pd.concat to concatenate the bank dataframes together to a single data frame called bank_stocks.
# Set the keys argument equal to the tickers list. Also pay attention to what axis you concatenate on
bank_stocks = pd.concat([df_BAC, df_C, df_GS, df_JPM, df_MS, df_WFC], axis=1, keys=tickers)
bank_stocks.columns.names = ['Bank Ticker', 'Stock Info']  # Set the column name levels
print('\n Close values of each bank:')
print(bank_stocks.xs(key='Close', axis=1, level='Stock Info').head())

# What is the max Close price for each bank's stock throughout the time period?
print('\n Max close value of each bank:\n', bank_stocks.xs(key='Close', axis=1, level='Stock Info').max())

# Creating empty dataframe to store bank returns
df_returns = pd.DataFrame()

# We can use pandas pct_change() method on the Close column to create a column representing this return value.
# Create a for loop that goes and for each Bank Stock Ticker creates this returns column and set's it as a column in
# the returns DataFrame.
for tick in tickers:
    df_returns[tick + 'returns'] = bank_stocks[tick]['Close'].pct_change()
print('\n Returns dataframe:\n', df_returns.head())
# print(df_returns[1:].head())  # Slicing dataframe to ignore NaN of first row

# Create a pairplot using seaborn of the returns dataframe. What stock stands out to you? Can you figure out why?
fig1 = sns.pairplot(df_returns[1:])
# plt.show()

# Using this returns DataFrame, figure out on what dates each bank stock had the best and worst single day returns.
# You should notice that 4 of the banks share the same day for the worst drop, did anything significant happen that day?
print('\n Worst day returns:\n', df_returns.idxmin())
print('\n Best day returns:\n', df_returns.idxmax())

# Take a look at the standard deviation of the returns, which stock would you classify as
# the riskiest over the entire time period?
# Which would you classify as the riskiest for the year 2015?
print('\nStandard deviations:\n', df_returns.std())
print('\n2015:\n', df_returns.loc['2015-01-01':'2015-12-31'].std())

# Create a distplot using seaborn of the 2015 returns for Morgan Stanley
print('\n2015 returns for Morgan Stanley:\n', df_returns['MSreturns'].loc['2015-01-01':'2015-12-31'].head())
fig2 = sns.displot(df_returns['MSreturns'].loc['2015-01-01':'2015-12-31'], kde=True)
# plt.show()

# ** Create a line plot showing Close price for each bank for the entire index of time.
# (Hint: Try using a for loop, or use .xs to get a cross section of the data.)**
fig3 = sns.lineplot(data = bank_stocks.xs(key='Close', axis=1, level='Stock Info'))
plt.show()

