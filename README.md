# CMF_DD
My work on a project "Data-driven approaches for predicting an asset price over a mid-term horison" in the Center of Mathematical Finances.

# Results
- Made a High Frequency Taking strategy that earns 12% daily yield with 15% MDD**.
- Running process and results - here https://github.com/ChistyakovArtem/CMF_HFMM/blob/main/Notebooks/ML_1-Stoikov-with-ML.ipynb.

# Strategy description
- Baseline of this strategy is a legendary https://math.nyu.edu/~avellane/HighFrequencyTrading.pdf article that allows to handle two market making risks - Adverse selection (if price is constantly decreasing - only bid orders will be executed - so we will only buy asset - resulting a loss) and Inventory risk - if we have large inventory - we will have a risk of losses due to price changes.

- However this strategy operates with current market statistics: midprice, order_intensity and volatility. But I will try to look in the future.
- This strategy involves a Light GBM with **linear_tree** and **early_stopping** to predict future **return** (**500ms horizon - correlation 0.19**) (by predicting return), future **order_intensity** (**2s horizon - correlation - 0.07**) and **future volatility** (**1s horizon - correlation 0.16**) based on previous orderbook states.

- Total pnl line is very stable.
