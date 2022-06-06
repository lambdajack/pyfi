from multiprocessing.dummy import Array
import time
import os
import csv
import yfinance as yf


def get_historic(tickers: Array):
    """
    This function will get the historic data for all tickers in the tickers array.

    Daily, hourly and five minute data is downloaded by default.

    Populate the tickers array below from a csv. Default is data/lists/USA-combined-tickers.csv
    """
    for t in tickers:
        print("Fetching data for " + t)

        five_minutely = yf.download(  # or pdr.get_data_yahoo(...
            tickers=t,
            period="60d",
            interval="5m",
        )
        hourly = yf.download(  # or pdr.get_data_yahoo(...
            tickers=t,
            period="60d",
            interval="1h",
        )
        daily = yf.download(  # or pdr.get_data_yahoo(...
            tickers=t,
            period="max",
            interval="1d",
        )

        p = os.path.join(os.getcwd(), "data", "stocks", t)
        os.makedirs(p, exist_ok=True)

        five_minutely.to_csv(os.path.join(p, f"{time.strftime('%Y-%m-%d')}_5m.csv"))
        hourly.to_csv(os.path.join(p, f"{time.strftime('%Y-%m-%d')}_1h.csv"))
        daily.to_csv(os.path.join(p, f"{time.strftime('%Y-%m-%d')}_1d.csv"))

        print("Saved data for " + t)

        time.sleep(2)


def append_tickers_from_csv(csvFile: str, tickers: Array):
    """
    Ticker symbols must be in the first column of the csv file.
    """
    with open(csvFile) as f:
        c = csv.reader(f)
        for row in c:
            if "ticker" in row[0].lower():
                print("Skipping header row")
                continue
            tickers.append(row[0])


tickers = []
append_tickers_from_csv(
    os.path.join(os.getcwd(), "data", "lists", "USA-combined-tickers.csv"), tickers
)
get_historic(tickers)
