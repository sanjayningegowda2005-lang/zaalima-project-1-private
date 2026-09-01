import os
import pandas as pd
import yfinance as yf


def fetch_zomato_data():
    print("Fetching live financial data for Zomato / Eternal (ETERNAL.NS)...")

    # Fetch ticker object from Yahoo Finance
    # Note: Eternal Ltd (formerly Zomato) uses ETERNAL.NS or ZOMATO.NS
    try:
        zomato = yf.Ticker("ETERNAL.NS")
        financials = zomato.financials
        if financials.empty:
            zomato = yf.Ticker("ZOMATO.NS")
            financials = zomato.financials
    except Exception:
        zomato = yf.Ticker("ZOMATO.NS")
        financials = zomato.financials

    if financials.empty:
        print("Failed to retrieve data. Check your internet connection.")
        return

    # Transpose so dates become rows and financial metrics become columns
    df_financials = financials.T

    # Ensure output directory exists
    os.makedirs("Data", exist_ok=True)

    # Display key financial indicators
    print("\n--- Financial Summary (Past Years) ---")
    print(df_financials.head())

    # Save raw extracted data into Data folder
    output_path = "Data/zomato_financials.csv"
    df_financials.to_csv(output_path)
    print(f"\nSuccessfully exported real financial dataset to: {output_path}")


if __name__ == "__main__":
    fetch_zomato_data()