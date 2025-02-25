import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# 下載過去10年的QQQ和VOO數據
end_date = datetime.now()
start_date = end_date - timedelta(days=3650)  # 約10年

qqq = yf.download("QQQ", start=start_date, end=end_date)
voo = yf.download("VOO", start=start_date, end=end_date)

# 計算月度收益率
qqq_monthly = qqq["Adj Close"].resample("M").last()
voo_monthly = voo["Adj Close"].resample("M").last()


# 計算相對強弱指標 (RSI)
def calculate_rsi(data, periods=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=periods).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=periods).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))


# 計算每月RSI
qqq_rsi = calculate_rsi(qqq_monthly)
voo_rsi = calculate_rsi(voo_monthly)

# 初始化投資組合
initial_investment = 10000
portfolio_value = initial_investment
holdings = "QQQ"  # 開始時持有QQQ
portfolio_values = []

# 回測策略
for i in range(len(qqq_monthly)):
    if i == 0:
        continue

    # RSI > 70 認為是高檔，轉換到VOO
    # RSI < 30 認為是低檔，轉換到QQQ
    if qqq_rsi[i] > 70 and holdings == "QQQ":
        holdings = "VOO"
    elif qqq_rsi[i] < 30 and holdings == "VOO":
        holdings = "QQQ"

    # 計算報酬率
    if holdings == "QQQ":
        returns = qqq_monthly[i] / qqq_monthly[i - 1]
    else:
        returns = voo_monthly[i] / voo_monthly[i - 1]

    portfolio_value *= returns
    portfolio_values.append(portfolio_value)

# 計算年化報酬率
years = (end_date - start_date).days / 365
annual_return = ((portfolio_value / initial_investment) ** (1 / years) - 1) * 100

print(f"初始投資: ${initial_investment:,.2f}")
print(f"最終投資組合價值: ${portfolio_value:,.2f}")
print(f"年化報酬率: {annual_return:.2f}%")

# 繪製投資組合價值變化圖


plt.figure(figsize=(12, 6))
plt.plot(portfolio_values)
plt.title("投資組合價值變化")
plt.xlabel("月份")
plt.ylabel("投資組合價值($)")
plt.grid(True)
plt.show()
