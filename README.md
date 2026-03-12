# USD to PKR Exchange Rate Analyzer

A Python command-line application that fetches and analyzes both real-time and historical exchange rates for the US Dollar (USD) to Pakistani Rupee (PKR).

## Features

- **Real-Time Exchange Rate**: Fetches the latest USD to PKR exchange rate from `x-rates.com`.
- **Currency Conversion**: Convert any amount of USD to PKR using the live exchange rate.
- **Historical Data Analysis**: Scrapes historical exchange rates from `currency-converter.org.uk` and saves them to a CSV file.
- **Historical Rate Lookup**: Find the exchange rate for any specific date in the past.
- **Historical Conversion**: Convert amounts based on the exchange rate of a specific historical date.
- **Identifying Highs and Lows**: Automatically scan historical data to find the highest and lowest ever recorded exchange rates.
- **Data Visualization**: Plot a line graph of the exchange rate over a user-specified date range using Matplotlib.
  
## How It Works

The script runs two background threads on startup:
1. One thread continuously fetches the real-time USD/PKR rate every 60 seconds.
2. Another thread scrapes the entire available historical exchange rate data and saves it locally as `usd_pkr_historical_data.csv`.

Once the historical data is ready, you'll be presented with an interactive terminal menu to perform your desired operations.

## Setup Instructions

### Prerequisites
Make sure you have Python 3 installed on your machine. You will also need `pip` to install the required dependencies.

### Installation

1. Clone this repository (or download the source code).
2. (Optional but recommended) Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
3. Install the required Python packages:
   ```bash
   pip install requests beautifulsoup4 pandas matplotlib
   ```

### Running the App

Execute the `main.py` script from your terminal:
```bash
python main.py
```

Wait a few seconds for the historical data to be successfully fetched, after which the main interactive menu will appear.
