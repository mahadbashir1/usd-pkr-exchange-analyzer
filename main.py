import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import threading
import time
import os

real_time_rate = 0.0
historical_data_ready = False

def fetch_real_time_rate():
    global real_time_rate
    while True:
        try:
            url = 'https://www.x-rates.com/calculator/?from=USD&to=PKR&amount=1'
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            rate = float(soup.find('span', class_='ccOutputRslt').text.split()[0])
            real_time_rate = rate
        except Exception as e:
            print(f"Error fetching real-time rate: {e}")
        time.sleep(60)

def fetch_and_save_historical_data():
    global historical_data_ready
    try:
        url = "https://www.currency-converter.org.uk/currency-rates/historical/table/USD-PKR.html"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        table = soup.find(id="content", class_="hfeed")
        rows = table.find_all('tr')[1:]
        dict = {
            "Date": [],
            "Rate": []
        }
        for i, row in enumerate(rows):
            row = rows[i]
            col = row.find_all('td')
            date = pd.to_datetime(col[1].get_text(), format='%d/%m/%Y')
            rate = float(col[3].get_text().split()[0].strip())
            dict["Date"].append(date)
            dict["Rate"].append(rate)
        df = pd.DataFrame(dict)
        df.to_csv("usd_pkr_historical_data.csv", index=False)
        historical_data_ready = True
        print("Historical data fetched and saved successfully.\n\n")
    except Exception as e:
        print(f"Error fetching historical data: {e}")

def view_real_time_rate():
    print(f"1 USD = {real_time_rate} PKR\n\n")

def convert():
    user_input = float(input("Enter the amount in USD you want to convert: "))
    print(f"{user_input} USD = {real_time_rate * user_input} PKR\n\n")

def fetch_historical_rate(date, df):
    return float(df.loc[df['Date'] == date, "Rate"].values[0])

def view_historical_rate(df):
    date = input("Enter date (YYYY-MM-DD): ")
    print(f"On {date}, 1 USD = {fetch_historical_rate(date, df)} PKR\n\n")

def historical_rate_conversion(df):
    user_input = float(input("Enter the amount in USD you want to convert: "))
    date = input("Enter date (YYYY-MM-DD): ")
    print(f"On {date}, {user_input} USD = {fetch_historical_rate(date, df) * user_input} PKR\n\n")

def identify_highs_lows(df):
    highest = df.loc[df['Rate'].idxmax()]
    lowest = df.loc[df['Rate'].idxmin()]
    print(f"Highest Exchange Rate: {highest['Rate']} PKR/USD on {highest['Date']}\n")
    print(f"Lowest Exchange Rate: {lowest['Rate']} PKR/USD on {lowest['Date']}\n\n")

def view_historical_data_for_specific_period(df):
    start_date = input("Enter Start date (YYYY-MM-DD): ")
    end_date = input("Enter End date (YYYY-MM-DD): ")
    filtered_df = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]
    plt.figure(figsize=(10, 5))
    plt.plot(filtered_df["Date"], filtered_df["Rate"], marker='o')
    plt.title(f'USD to PKR Exchange Rate from {start_date} to {end_date}')
    plt.xlabel('Date')
    plt.ylabel('Exchange Rate (PKR)')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def main_menu():
    print("Currency Exchange Rate Analyzer")
    print("1. View Real-Time Exchange Rate")
    print("2. Convert Currency")
    print("3. View Historical Exchange Rate")
    print("4. View Historical Data for a specific period")
    print("5. Historical Rate Conversion")
    print("6. Identify Highs and Lows")
    print("7. Exit")
    return input("Please enter your choice: ")

def main():
    global real_time_rate
    global historical_data_ready

    rate_thread = threading.Thread(target=fetch_real_time_rate, daemon=True)
    rate_thread.start()

    historical_thread = threading.Thread(target=fetch_and_save_historical_data, daemon=True)
    historical_thread.start()

    while not historical_data_ready:
        print("Fetching historical data, please wait...")
        time.sleep(2)
    
    file_path = "usd_pkr_historical_data.csv"
    df = pd.read_csv(file_path, encoding='utf-8')

    while True:
        choice = main_menu()
        os.system('cls')
        if choice == '1':
            view_real_time_rate()
        elif choice == '2':
            convert()
        elif choice == '3':
            view_historical_rate(df)
        elif choice == '4':
            view_historical_data_for_specific_period(df)
        elif choice == '5':
            historical_rate_conversion(df)
        elif choice == '6':
            identify_highs_lows(df)
        elif choice == '7':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
