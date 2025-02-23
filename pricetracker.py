import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import subprocess

# Data sources (example placeholders, update with actual APIs)
EGG_PRICE_URL = "https://www.usda.gov/data/bureau-labor-statistics/download-data"  # Replace with USDA/BLS API
GAS_PRICE_URL = "https://gasprices.aaa.com/?state=PA"  # Replace with AAA/EIA API
DATA_FILE = "price_data.csv"

# Function to fetch data (replace with actual API calls)
def fetch_prices():
    try:
        # Simulating API responses (Replace with actual API calls)
        egg_price = requests.get(EGG_PRICE_URL).json()["average_weekly_price"]
        gas_price = requests.get(GAS_PRICE_URL).json()["average_weekly_price"]
        return egg_price, gas_price
    except Exception as e:
        print("Error fetching prices:", e)
        return None, None

# Function to update CSV
def update_data():
    egg_price, gas_price = fetch_prices()
    if egg_price is None or gas_price is None:
        return

    today = datetime.date.today()
    new_entry = pd.DataFrame({"date": [today], "egg_price": [egg_price], "gas_price": [gas_price]})
    
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df = pd.concat([df, new_entry], ignore_index=True)
    else:
        df = new_entry

    df.to_csv(DATA_FILE, index=False)
    return df

# Function to generate the chart
def generate_chart():
    df = pd.read_csv(DATA_FILE)
    df["date"] = pd.to_datetime(df["date"])
    df.sort_values("date", inplace=True)

    plt.figure(figsize=(10, 5))
    plt.plot(df["date"], df["egg_price"], label="Egg Price ($/dozen)", marker="o")
    plt.plot(df["date"], df["gas_price"], label="Gas Price ($/gallon)", marker="s")
    
    # Annotate latest prices
    latest_date = df["date"].iloc[-1]
    latest_egg_price = df["egg_price"].iloc[-1]
    latest_gas_price = df["gas_price"].iloc[-1]
    plt.annotate(f"${latest_egg_price}", (latest_date, latest_egg_price), textcoords="offset points", xytext=(0,10), ha='center')
    plt.annotate(f"${latest_gas_price}", (latest_date, latest_gas_price), textcoords="offset points", xytext=(0,10), ha='center')
    
    plt.xlabel("Date")
    plt.ylabel("Price ($)")
    plt.title("Weekly Average Egg & Gas Prices")
    plt.legend()
    plt.grid()
    
    chart_file = "price_chart.png"
    plt.savefig(chart_file)
    plt.close()
    return chart_file

# Function to send iMessage
def send_imessage():
    chart_file = generate_chart()
    phone_number = "+17174058896"  # Replace with recipient's number
    message = "Here’s your daily price update! 📊"
    
    applescript = f'''
    set imagePath to POSIX file "{os.path.abspath(chart_file)}"
    set phoneNumber to "{phone_number}"
    tell application "Messages"
        set theBuddy to buddy phoneNumber of service "SMS"
        send imagePath to theBuddy
        send "{message}" to theBuddy
    end tell
    '''
    
    subprocess.run(["osascript", "-e", applescript])

# Run daily update and message
if __name__ == "__main__":
    update_data()
    send_imessage()
