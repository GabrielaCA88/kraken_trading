# kraken_trading

1. miner.py
Class Tradedata:

a. instantiates pykrakenapi 
b. get_data: drops vwap generated by the API and assigns a new one based on the analytical calculation. 
returns the modified pandas df. 

2. app.py

this is a Dash app wit HTML and Dash Core components. For UI purposes, I also included dash bootstrap components. 
The layout contains a title, a description, dropdown to select pair of coins, date picker to determine the date since when the information needs to be retrieved, the timeframe interval of the data (minutes, days and weeks), the graph representing the information selected and three buttons to specific sources of information of the crypto world. 

The Dahs is interactive with three callbacks impacting on the graph. 

Last but not least, I use plotly to plot the information in the classical japanese candlesticks together with the vwap calculated with miner.py.  

Future project: include timezones, further clean the code and improve the UI.  
