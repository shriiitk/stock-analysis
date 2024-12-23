import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import timedelta
import argparse
import sys

def fetch_stock_data(ticker_name, history_period):
    """
    Fetch stock data using the yfinance library.
    """
    try:
        ticker = yf.Ticker(ticker_name)
        data = ticker.history(period=history_period, interval="1d")
    except Exception as e:
        print(f"Error fetching data for ticker '{ticker_name}': {e}")
        sys.exit(1)

    # Reset index and format the data
    data.reset_index(inplace=True)
    data = data[['Date', 'Open']]
    data.rename(columns={'Open': 'Opening Price'}, inplace=True)
    data['Date'] = pd.to_datetime(data['Date'])
    data['Date'] = data['Date'].dt.strftime('%Y-%m-%d')
    return data

def process_stock_data(data, num_months, ticker_name, history_period):
    """
    Process stock data to analyze best buy and sell dates.
    """
    # Ensure proper formatting of columns
    data['Date'] = pd.to_datetime(data['Date'])
    data.sort_values('Date', inplace=True)
    data['YearMonth'] = data['Date'].dt.to_period('M').astype(str)

    # Analyze each month for best buy dates
    results = []
    for group, monthly_data in data.groupby('YearMonth'):
        monthly_avg = monthly_data['Opening Price'].mean()
        low_price_days = monthly_data[monthly_data['Opening Price'] < monthly_avg]
        low_price_days = low_price_days.nsmallest(3, 'Opening Price')
        for _, row in low_price_days.iterrows():
            results.append({
                'Date': row['Date'],
                'Opening Price': row['Opening Price'],
                'Month': group
            })

    # Save historical best buy dates
    results_df = pd.DataFrame(results)
    historical_output_file = f"{ticker_name}_{history_period}_best_buy_dates.csv"
    results_df.to_csv(historical_output_file, index=False)
    print(f"Historical best buy dates saved to '{historical_output_file}'.")

    # Predict future prices
    last_date = data['Date'].max()
    recent_stats = data.tail(90)['Opening Price']  # Use last 90 days for trend analysis
    recent_avg = recent_stats.mean()
    recent_std = recent_stats.std()
    trend = (recent_stats.iloc[-1] - recent_stats.iloc[0]) / len(recent_stats)  # Price change per day

    future_dates = pd.date_range(start=last_date + timedelta(days=1), periods=num_months * 30)

    future_data = []
    for future_date in future_dates:
        month_key = f"{future_date.year}-{future_date.month:02d}"
        avg_price = recent_avg + trend * (future_date - last_date).days
        volatility = recent_std
        simulated_price = np.random.normal(avg_price, volatility)
        simulated_price = max(simulated_price, recent_avg * 0.8)  # Avoid very low prices
        simulated_price = min(simulated_price, recent_avg * 1.2)  # Avoid overly high prices
        future_data.append({'Date': future_date, 'Opening Price': simulated_price})

    future_df = pd.DataFrame(future_data)
    future_df['YearMonth'] = future_df['Date'].dt.to_period('M').astype(str)

    # Predict best buy and sell dates
    predicted_buy_results = []
    predicted_sell_results = []

    for group, monthly_data in future_df.groupby('YearMonth'):
        monthly_avg = monthly_data['Opening Price'].mean()

        # Best Buy Dates: Lowest 3 prices
        low_price_days = monthly_data[monthly_data['Opening Price'] <= monthly_avg]
        low_price_days = low_price_days.nsmallest(3, 'Opening Price')
        for _, row in low_price_days.iterrows():
            predicted_buy_results.append({
                'Date': row['Date'],
                'Opening Price': row['Opening Price'],
                'Month': group
            })

        # Best Sell Dates: Highest 3 prices
        high_price_days = monthly_data.nlargest(3, 'Opening Price')
        for _, row in high_price_days.iterrows():
            predicted_sell_results.append({
                'Date': row['Date'],
                'Opening Price': row['Opening Price'],
                'Month': group
            })

    # Save predicted best buy and sell dates
    predicted_buy_df = pd.DataFrame(predicted_buy_results)
    predicted_sell_df = pd.DataFrame(predicted_sell_results)

    predicted_buy_file = f"{ticker_name}_{history_period}_predicted_best_buy_dates.csv"
    predicted_sell_file = f"{ticker_name}_{history_period}_predicted_best_sell_dates.csv"

    predicted_buy_df.to_csv(predicted_buy_file, index=False)
    predicted_sell_df.to_csv(predicted_sell_file, index=False)

    print(f"Predicted best buy dates saved to '{predicted_buy_file}'.")
    print(f"Predicted best sell dates saved to '{predicted_sell_file}'.")

    # Visualization
    plt.figure(figsize=(12, 6))
    plt.scatter(results_df['Date'], results_df['Opening Price'], color='blue', label='Historical Best Buy Dates', zorder=5)
    plt.scatter(predicted_buy_df['Date'], predicted_buy_df['Opening Price'], color='green', label='Predicted Best Buy Dates', zorder=5)
    plt.scatter(predicted_sell_df['Date'], predicted_sell_df['Opening Price'], color='red', label='Predicted Best Sell Dates', zorder=5)
    plt.xlabel('Date')
    plt.ylabel('Opening Price')
    plt.title(f'Historical and Predicted Best Buy/Sell Dates for {ticker_name}')
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Fetch stock data and analyze best buy/sell dates.")
    parser.add_argument("ticker", type=str, help="Yahoo Finance ticker symbol.")
    parser.add_argument("history_period", type=str, help="Time period for historical data (e.g., '5y', '1y').")
    parser.add_argument("num_months", type=int, help="Number of months to predict future best buy/sell dates.")
    args = parser.parse_args()

    # Fetch stock data
    print(f"Fetching data for ticker '{args.ticker}' with history period '{args.history_period}'...")
    stock_data = fetch_stock_data(args.ticker, args.history_period)

    # Save fetched data to CSV
    input_csv_file = f"{args.ticker}_{args.history_period}_data.csv"
    stock_data.to_csv(input_csv_file, index=False)
    print(f"Fetched stock data saved to '{input_csv_file}'.")

    # Process stock data
    process_stock_data(stock_data, args.num_months, args.ticker, args.history_period)

if __name__ == "__main__":
    main()
