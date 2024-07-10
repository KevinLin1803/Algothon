import numpy as np

##### TODO #########################################
### RENAME THIS FILE TO YOUR TEAM NAME #############
### IMPLEMENT 'getMyPosition' FUNCTION #############
### TO RUN, RUN 'eval.py' ##########################

nInst = 50
currentPos = np.zeros(nInst)
pricePos = np.zeros(nInst)

def calculate_ema(prices, window):
    ''' Calculating the Exponential Moving Average (EMA) '''
    ema = np.zeros_like(prices)
    alpha = 2 / (window + 1)
    ema[0] = prices[0]
    for i in range(1, len(prices)):
        ema[i] = alpha * prices[i] + (1 - alpha) * ema[i - 1]
    return ema

def calculate_rsi(prices, window):
    ''' Calculating the Relative Strength Index (RSI) '''
    deltas = np.diff(prices)
    seed = deltas[:window]
    up = seed[seed >= 0].sum() / window
    down = -seed[seed < 0].sum() / window
    rs = up / down
    rsi = np.zeros_like(prices)
    rsi[:window] = 100. - 100. / (1. + rs)
    
    for i in range(window, len(prices)):
        delta = deltas[i - 1]
        if delta > 0:
            up_val = delta
            down_val = 0.
        else:
            up_val = 0.
            down_val = -delta
        up = (up * (window - 1) + up_val) / window
        down = (down * (window - 1) + down_val) / window
        rs = up / down
        rsi[i] = 100. - 100. / (1. + rs)
    return rsi


def calculate_cci(prices, window):
    ''' Calculating for the Commodity Channel Index (CCI) '''
    typical_price = (prices[:, -window:].sum(axis=0)) / window
    mean_deviation = np.mean(np.abs(prices[:, -window:] - typical_price), axis=0)
    cci = (typical_price - np.mean(typical_price)) / (0.015 * np.mean(mean_deviation))
    return cci


def getMyPosition(prcSoFar):
    global currentPos, pricePos
    (nins, nt) = prcSoFar.shape
    if nt < 2:
        return np.zeros(nins)
    
    # EMA Variables (can change the windows)
    ema_short_window = 10
    ema_long_window = 12
    
    # RSI Variables (can change the window and thresholds)
    rsi_window = 21
    rsi_buy_threshold = 50
    rsi_sell_threshold = 50
    
    # CCI Variables (can change the windows and threshold)
    cci_window = 100
    cci_buy_threshold = 50
    cci_sell_threshold = 50

    for i in range(nins):
        prices = prcSoFar[i, :]
        ema_short = calculate_ema(prices, ema_short_window)
        ema_long = calculate_ema(prices, ema_long_window)
        rsi = calculate_rsi(prices, rsi_window)
        cci = calculate_cci(prcSoFar, cci_window)

        # Calculate volatility
        volatility = np.std(prices[-ema_short_window:])
        if volatility == 0: 
            volatility = 1

        # Buy signal -- if ema(10) > ema(12) AND rsi(21) < 50 and CCI(100) < 50
        if ema_short[-1] > ema_long[-1] and rsi[-1] > rsi_buy_threshold and cci[-1] > cci_buy_threshold:
            currentPos[i] += 10

        # Sell signal
        elif ema_short[-1] < ema_long[-1] and rsi[-1] < rsi_sell_threshold and cci[-1] < cci_sell_threshold:
            currentPos[i] -= 10 / volatility

        # Hold Signal
        else:
            currentPos[i] += 0

    return currentPos
