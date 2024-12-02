# Stock Analysis Utility

A Python script to fetch historical stock prices, analyze best buy dates, and predict future best buy dates for any stock using Yahoo Finance data.

---

## Features

1. Fetch historical stock data for a given ticker and period.
2. Analyze historical best buy and sell dates for each month.
3. Predict future best buy and sell dates for the next specified number of months.
4. Generate CSV files for historical and predicted best buy & sell dates.
5. Display a plot visualizing historical and predicted trends.

---

## Installation and Usage

### Prerequisites

- Python 3.7 or later installed on your system.
- Basic understanding of command-line operations.

---

### Setup Instructions

1. **Clone the Repository**  
   Clone the repository to your local system:
   ```bash
   git clone https://github.com/shriiitk/stock-analysis.git
   cd stock-analysis
   ```

2. **Create a Virtual Environment**  
   Create a virtual environment named `stocks`:
   ```bash
   python -m venv stocks
   ```

3. **Activate the Virtual Environment**
   - **Windows**:
     ```bash
     stocks\Scripts\activate
     ```
   - **Mac/Linux**:
     ```bash
     source stocks/bin/activate
     ```

4. **Install Required Dependencies**  
   Install all necessary libraries:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Script**  
   Execute the script with the required arguments:
   ```bash
   python stock_analysis.py <ticker_name> <history_period> <num_months>
   ```
   - `<ticker_name>`: Stock ticker symbol (e.g., `^NSEI` for NIFTY 50).
   - `<history_period>`: Period of historical data (e.g., `5y` for 5 years).
   - `<num_months>`: Number of future months to predict best buy dates.

   Example:
   ```bash
   python stock_analysis.py ^NSEI 5y 3
   ```

---

## Output

1. **Historical Stock Data:**  
   `<ticker>_<history_period>_data.csv`

2. **Historical Best Buy Dates:**  
   `<ticker>_<history_period>_best_buy_dates.csv`

3. **Predicted Best Buy Dates:**  
   `<ticker>_<history_period>_predicted_best_buy_dates.csv`

4. **Visualization Plot:**  
   A plot showing historical and predicted best buy dates.

---

## Example Usage

To analyze NIFTY 50 data for the past 5 years and predict best buy dates for the next 3 months:
```bash
python stock_analysis.py ^NSEI 5y 3
```

---

## Contributing

Feel free to fork the repository, make changes, and create a pull request for review.

---

## License

This project is licensed under the MIT License.
