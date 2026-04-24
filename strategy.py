import yfinance as yf

def get_data(symbol):
    return yf.download(symbol, period="1mo", interval="1h")

def analyze(symbol):
    df = get_data(symbol)

    if df.empty:
        return None

    df["MA50"] = df["Close"].rolling(50).mean()

    last = df.iloc[-1]

    support = df["Low"].rolling(20).min().iloc[-2]
    resistance = df["High"].rolling(20).max().iloc[-2]

    trend_up = last["Close"] > last["MA50"]

    volume_spike = last["Volume"] > df["Volume"].mean() * 1.5
    strong_candle = abs(last["Close"] - last["Open"]) > df["Close"].std()

    breakout = last["Close"] > resistance

    retest = (last["Low"] <= resistance) and (last["Close"] > resistance)

    if trend_up and breakout and volume_spike and strong_candle and retest:

        return {
            "symbol": symbol,
            "type": "CALL",
            "entry": round(last["Close"], 2),
            "support": round(support, 2),
            "resistance": round(resistance, 2),
        }

    return None
