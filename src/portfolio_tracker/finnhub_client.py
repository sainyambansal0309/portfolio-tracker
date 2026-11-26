import os
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("FINNHUB_API_KEY")
BASE_URL = "https://finnhub.io/api/v1"


def get_quote(symbol: str) -> tuple[float, str]:
    """Return the latest price and its timestamp from Finnhub."""
    if not API_KEY:
        raise RuntimeError("FINNHUB_API_KEY is missing. Add it to your .env file.")

    response = requests.get(
        f"{BASE_URL}/quote",
        params={"symbol": symbol},
        headers={"X-Finnhub-Token": API_KEY},
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()

    if not data.get("c"):
        raise ValueError(f"No Finnhub data for {symbol}")

    when = datetime.fromtimestamp(data["t"], tz=timezone.utc)
    return float(data["c"]), when.strftime("%Y-%m-%d %H:%M UTC")


if __name__ == "__main__":
    for symbol in ["AAPL", "RELIANCE.NS"]:
        try:
            price, when = get_quote(symbol)
            print(f"{symbol}: {price:.2f}  (as of {when})")
        except Exception as error:
            print(f"{symbol}: failed -> {error}")