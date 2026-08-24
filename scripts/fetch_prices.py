#!/usr/bin/env python3
"""
Fetch latest closing prices for all codes in seed500.txt.
Primary source: FinMind API (JSON, real-time-ish daily close).
Fallback source: Yahoo Finance chart JSON API (regularMarketPrice),
tried against both the listed (.TW) and OTC (.TWO) suffixes.

This replaces the old WebFetch+LLM-prompt approach with plain HTTP + JSON
parsing, so it can run unattended inside GitHub Actions with no LLM in
the loop. Writes results as "code|price" lines to fresh_prices.txt so
merge500.py can consume them exactly as before.
"""
import sys
import time
import json
import datetime
import urllib.request
import urllib.error

SEED_PATH = sys.argv[1] if len(sys.argv) > 1 else "/tmp/seed500.txt"
OUT_PATH = sys.argv[2] if len(sys.argv) > 2 else "/tmp/fresh_prices.txt"

REQUEST_TIMEOUT = 10
MAX_RETRIES = 2
RETRY_SLEEP = 1.5
BETWEEN_REQUESTS_SLEEP = 0.15

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; tpex500-bot/1.0; +https://github.com/yanhsu/tpex500)"
}


def http_get_json(url, timeout=REQUEST_TIMEOUT):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_finmind(code, start_date):
    url = (
        "https://api.finmindtrade.com/api/v4/data"
        f"?dataset=TaiwanStockPrice&data_id={code}&start_date={start_date}"
    )
    data = http_get_json(url)
    rows = data.get("data") or []
    if not rows:
        return None
    rows.sort(key=lambda r: r.get("date", ""))
    last = rows[-1]
    close = last.get("close")
    if close is None:
        return None
    try:
        return float(close)
    except (TypeError, ValueError):
        return None


def fetch_yahoo(code):
    for suffix in (".TW", ".TWO"):
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{code}{suffix}"
        try:
            data = http_get_json(url)
        except Exception:
            continue
        try:
            result = data["chart"]["result"][0]
            price = result["meta"].get("regularMarketPrice")
            if price is not None:
                return float(price)
        except (KeyError, IndexError, TypeError, ValueError):
            continue
    return None


def fetch_with_retries(fn, *args):
    for attempt in range(MAX_RETRIES):
        try:
            price = fn(*args)
            if price is not None:
                return price
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError):
            pass
        if attempt < MAX_RETRIES - 1:
            time.sleep(RETRY_SLEEP)
    return None


def load_codes(seed_path):
    codes = []
    with open(seed_path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.strip():
                continue
            code = line.split("|", 1)[0].strip()
            if code:
                codes.append(code)
    return codes


def main():
    codes = load_codes(SEED_PATH)
    start_date = (datetime.date.today() - datetime.timedelta(days=7)).isoformat()

    refreshed = 0
    fallback = 0
    with open(OUT_PATH, "a", encoding="utf-8") as out:
        for i, code in enumerate(codes, 1):
            price = fetch_with_retries(fetch_finmind, code, start_date)
            source = "finmind"
            if price is None:
                price = fetch_with_retries(fetch_yahoo, code)
                source = "yahoo"
            if price is not None:
                out.write(f"{code}|{price}\n")
                out.flush()
                refreshed += 1
            else:
                fallback += 1
                print(f"[{i}/{len(codes)}] {code}: no fresh price (finmind+yahoo failed), will use seed value")

            if i % 25 == 0:
                print(f"[{i}/{len(codes)}] progress: refreshed={refreshed} pending_fallback={fallback}")

            time.sleep(BETWEEN_REQUESTS_SLEEP)

    print(f"DONE codes={len(codes)} refreshed={refreshed} no_fresh_price={fallback} source_last={source if codes else 'n/a'}")


if __name__ == "__main__":
    main()
