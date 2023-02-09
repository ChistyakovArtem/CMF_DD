# CMF_DD
My work on a project "Data-driven approaches for predicting an asset price over a mid-term horison" in the Center of Mathematical Finances.

# Results
- Made a High Frequency Taking strategy that earns **12% daily yield with 15% MDD**.
- Running process and results - here https://github.com/ChistyakovArtem/CMF_DD/tree/main/Taking.

# Strategy description
- This strategy predicts return short-term(500ms) / very-short(10ms). And longs/shorts asset based on this prediction. If the expected profit is greater than fees - we buy. If the expected loss is less than fees - we sell.
- I used multiple rolling features including volume history, previous prices (return) - and achieved total **correlation between prediction and midprice = 0.2**. 
