#!/usr/bin/env python3
"""Fetch 20-year daily stock prices from Alpha Vantage and save as CSV."""

import csv
import os
import time
import urllib.request
import json

# --- Configuration -----------------------------------------------------------
API_KEY_FILE = os.path.join(os.path.dirname(__file__), "api.key")
SYMBOLS = ["AAPL", "AMZN", "CRAY", "CSCO", "HPQ", "IBM", "INTC", "MSFT", "NVDA", "ORCL"]
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "stock_data")
WAIT_SECONDS = 13  # free tier: 5 calls/min → ~12 s between calls
# ---------------------------------------------------------------------------

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Read API key
with open(API_KEY_FILE) as f:
    API_KEY = f.read().strip()

BASE_URL = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&outputsize=full&datatype=json&apikey={apikey}&symbol={symbol}"


def fetch_daily(symbol: str) -> dict:
    """Return JSON response for a symbol."""
    url = BASE_URL.format(apikey=API_KEY, symbol=symbol)
    print(f"[{symbol}] Fetching …", end=" ", flush=True)
    with urllib.request.urlopen(url) as resp:
        data = json.loads(resp.read().decode())
    key = "Time Series (Daily)"
    if key not in data:
        print(f"ERROR: {data.get('Note', data.get('Error Message', data))}")
        return {}
    print(f"{len(data[key])} records")
    return data[key]


def save_csv(symbol: str, series: dict):
    """Write series to CSV with the requested columns."""
    path = os.path.join(OUTPUT_DIR, f"{symbol}.csv")
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["timestamp", "open", "high", "low", "close",
                     "adjusted_close", "volume", "dividend_amount",
                     "split_coefficient"])
        for ts, fields in sorted(series.items(), reverse=True):
            w.writerow([
                ts,
                fields.get("1. open", ""),
                fields.get("2. high", ""),
                fields.get("3. low", ""),
                fields.get("4. close", ""),
                fields.get("5. adjusted close", ""),
                fields.get("6. volume", ""),
                fields.get("7. dividend amount", ""),
                fields.get("8. split coefficient", ""),
            ])
    print(f"  Saved → {path}")


def main():
    for i, sym in enumerate(SYMBOLS):
        series = fetch_daily(sym)
        if series:
            save_csv(sym, series)
        # Rate-limit: wait between calls (skip wait after last symbol)
        if i < len(SYMBOLS) - 1:
            print(f"  Waiting {WAIT_SECONDS}s for rate limit …")
            time.sleep(WAIT_SECONDS)
    print("\nDone. Files in", OUTPUT_DIR)


if __name__ == "__main__":
    main()
