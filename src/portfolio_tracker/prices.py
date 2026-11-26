import yfinance as yf


def get_latest_price(symbol: str) -> tuple[float, str]:
    """Return the most recent price and its timestamp for a stock symbol."""
    history = yf.Ticker(symbol).history(period="1d", interval="1m")
    if history.empty:
        history = yf.Ticker(symbol).history(period="5d")
    if history.empty:
        raise ValueError(f"No price data found for {symbol}")
    last_time = history.index[-1].strftime("%Y-%m-%d %H:%M %Z")
    return float(history["Close"].iloc[-1]), last_time


if __name__ == "__main__":
    for symbol in ["AAPL", "RELIANCE.NS"]:
        price, when = get_latest_price(symbol)
        print(f"{symbol}: {price:.2f}  (as of {when})")