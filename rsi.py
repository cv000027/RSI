#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 21:46:25 2021

@author: caojiajia
"""



import pandas as pd
import pandas_datareader as web
import matplotlib.pyplot as plt
import datetime as dt


ticker = "2330.TW"  # 輸入股票代號（這邊用台積電）
start = dt.datetime(2021,1,1) #設定開始時間
end = dt.datetime.now()  #設定結束時間或是直接設定為當下時間


data = web.DataReader(ticker, "yahoo", start, end)  # 抓取yahoo股市上的資料
closing_data = data["Adj Close"] 

#計算今天和昨天調整後的收盤價之間的差異。
delta_closing_data = closing_data.diff(1)  # 計算今天和昨天收盤價的差異
delta_closing_data = delta_closing_data.dropna(inplace = False)  #刪除不能用的值
#inplace = False 直接修改資料

positive = delta_closing_data.copy()
negative = delta_closing_data.copy()
positive[positive < 0 ] = 0
negative[negative > 0] = 0
#上面幾行的意思是如果前一天有跌的話，positive = 0，前一天漲，negative = 0
days = 14     #RSI顯示的日期天數 

#計算公式：RSI = 100 －（ 100 ／　( 1 + RS ) ）
# RS = 期間內的漲幅平均/期間內跌幅平均的絕對值

average_gain = positive.rolling(window = days).mean()  #漲幅的平均值 
average_loss = abs(negative.rolling(window = days).mean())   #跌幅的平均值的“絕對值”
 
relative_strength = average_gain / average_loss
rsi = 100.0 - (100.0 / (1.0 + relative_strength)) 

#組合前面完成的dataframe
combined = pd.DataFrame()
combined['Adj Close'] = data['Adj Close']
combined['rsi'] = rsi                        


#開始畫圖摟！
#收盤價圖表
plt.figure(figsize = (12, 8))
axis_1 = plt.subplot(211)

axis_1.plot(combined.index, combined["Adj Close"], color = "lightgray") #結合時間跟x軸
axis_1.set_title("Closing Share Price", color = "black")
axis_1.grid(True, color = "#555555") #顯示網格線 
axis_1.set_axisbelow(True)
axis_1.set_facecolor("black")
axis_1.tick_params(axis = "x", colors = "black") #顯示x y 軸上的數字 
axis_1.tick_params(axis = "y", colors = "black")                  

#RSI圖表
axis_2 = plt.subplot(212, sharex = axis_1)  # 兩個圖表共用同一個x軸（日期）

axis_2.plot(combined.index, combined["rsi"], color = "lightgray")    #每間隔10畫一個隔線
axis_2.axhline(0, linestyle = "--", alpha = 0.5, color = "#ff0000")
axis_2.axhline(10, linestyle = "--", alpha = 0.5, color = "#ffaa00")
axis_2.axhline(20, linestyle = "--", alpha = 0.5, color = "#00ff00")
axis_2.axhline(30, linestyle = "--", alpha = 0.5, color = "#cccccc")
axis_2.axhline(70, linestyle = "--", alpha = 0.5, color = "#cccccc")
axis_2.axhline(80, linestyle = "--", alpha = 0.5, color = "#00ff00")
axis_2.axhline(90, linestyle = "--", alpha = 0.5, color = "#ffaa00")
axis_2.axhline(100, linestyle = "--", alpha = 0.5, color = "#ff0000")

axis_2.set_title("RSI", color = "black")
axis_2.grid(False)   #擦掉網格線不然圖看起來很亂
axis_2.set_axisbelow(True)
axis_2.set_facecolor("black")




axis_2.tick_params(axis = "x", colors = "black") #有標數字的地方突出一點點數線方便閱讀
axis_2.tick_params(axis = "y", colors = "black")              


plt.show()                              