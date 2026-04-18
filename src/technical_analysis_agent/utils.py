# slackers_trading_agent/src/technical_analysis_agent/utils.py

import pandas as pd

def prepare_ta_markdown(df: pd.DataFrame, window: int = 15) -> str:
    cols_to_round = {
        'open': 1, 'high': 1, 'low': 1, 'close': 1,
        'RSI': 2, 'MACD_12_26_9': 2, 'MACDh_12_26_9': 2, 'MACDs_12_26_9': 2,
        'BBL_20_2.0_2.0': 2, 'BBM_20_2.0_2.0': 2, 'BBU_20_2.0_2.0': 2,
        'BBB_20_2.0_2.0': 2, 'BBP_20_2.0_2.0': 2
    }

    df = df.tail(window).round(cols_to_round).fillna("N/A")

    return df.to_markdown(index=False)