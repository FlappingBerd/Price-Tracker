import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import argparse
from bs4 import BeautifulSoup
import time

# Data file
DATA_FILE = "price_tracker.csv"

# Function to fetch egg prices (using web scraping as a placeholder)
def fetch_egg_price():
    try:
        # This is a placeholder - in reality, you'd want to use an official API
        # or find a reliable data source for egg prices
        response = requests.get("https://www.ams.usda.gov/market-news/egg-market-news-reports")
        if response.status_code == 200:
            # This is simplified - you'd need proper parsing logic
            # based on the actual page structure
            soup = BeautifulSoup(response.text, 'html.parser')
            # Example: Look for a specific table or element containing the price
            # price_element = soup.find("div", class_="price-element")
            # return float(price_element.text.strip().replace("$", ""))
            
            # For testing, return a random price between $2.50 and $4.00
            import random
            return round(random.uniform(2.50, 4.00), 2)
        else:
            print(f"Failed to fetch egg price: HTTP {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching egg price: {e}")
        return None

# Function to fetch gas prices (using web scraping as a placeholder)
def fetch_gas_price():
    try:
        # This is a placeholder - in reality, you should use an official API
        response = requests.get("https://gasprices.aaa.com/?state=PA")
        if response.status_code == 200:
            # This is simplified - you'd need proper parsing logic
            soup = BeautifulSoup(response.text, 'html.parser')
            # Example: Find the element containing the price
            # price_element = soup.find("span", class_="current-price")
            # return float(price_element.text.strip().replace("$", ""))
            
            # For testing, return a random price between $3.00 and $4.50
            import random
            return round(random.uniform(3.00, 4.50), 2)
        else:
            print(f"Failed to fetch gas price: HTTP {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching gas price: {e}")
        return None

# Function to update CSV
def update_data():
    egg_price = fetch_egg_price()
    gas_price = fetch_gas_price()
    
    if egg_price is None and gas_price is None:
        print("Failed to fetch both egg and gas prices. No update made.")
        return None
    
    today = datetime.date.today()
    
    # Create a dictionary for the new entry
    new_data = {"date": today}
    if egg_price is not None:
        new_data["egg_price"] = egg_price
    if gas_price is not None:
        new_data["gas_price"] = gas_price
    
    new_entry = pd.DataFrame([new_data])
    
    # Load existing data or create new dataframe
    if os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0:
        try:
            df = pd.read_csv(DATA_FILE)
            # Convert date column to datetime
            df["date"] = pd.to_datetime(df["date"])
            # Append new data
            df = pd.concat([df, new_entry], ignore_index=True)
        except Exception as e:
            print(f"Error reading existing data file: {e}")
            df = new_entry
    else:
        df = new_entry
    
    # Save the updated dataframe
    df.to_csv(DATA_FILE, index=False)
    print(f"Data updated for {today}")
    return df

# Function to generate the chart
def generate_chart():
    if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
        print("No data available to generate chart.")
        return None
    
    try:
        df = pd.read_csv(DATA_FILE)
        if len(df) < 1:
            print("Not enough data points to generate a chart.")
            return None
        
        df["date"] = pd.to_datetime(df["date"])
        df.sort_values("date", inplace=True)
        
        plt.figure(figsize=(12, 6))
        
        # Plot egg prices if available
        if "egg_price" in df.columns and not df["egg_price"].isnull().all():
            plt.plot(df["date"], df["egg_price"], label="Egg Price ($/dozen)", marker="o", color="brown")
            # Annotate latest egg price
            latest_idx = df["egg_price"].last_valid_index()
            if latest_idx is not None:
                latest_date = df["date"].iloc[latest_idx]
                latest_egg_price = df["egg_price"].iloc[latest_idx]
                plt.annotate(f"${latest_egg_price:.2f}", 
                             (latest_date, latest_egg_price), 
                             textcoords="offset points", 
                             xytext=(0,10), 
                             ha='center')
        
        # Plot gas prices if available
        if "gas_price" in df.columns and not df["gas_price"].isnull().all():
            plt.plot(df["date"], df["gas_price"], label="Gas Price ($/gallon)", marker="s", color="blue")
            # Annotate latest gas price
            latest_idx = df["gas_price"].last_valid_index()
            if latest_idx is not None:
                latest_date = df["date"].iloc[latest_idx]
                latest_gas_price = df["gas_price"].iloc[latest_idx]
                plt.annotate(f"${latest_gas_price:.2f}", 
                             (latest_date, latest_gas_price), 
                             textcoords="offset points", 
                             xytext=(0,10), 
                             ha='center')
        
        plt.xlabel("Date")
        plt.ylabel("Price ($)")
        plt.title("Weekly Average Egg & Gas Prices")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        # Format x-axis dates
        plt.gcf().autofmt_xdate()
        
        chart_file = "price_chart.png"
        plt.savefig(chart_file, dpi=300)
        plt.close()
        print(f"Chart saved to {chart_file}")
        return chart_file
    
    except Exception as e:
        print(f"Error generating chart: {e}")
        return None

# Function to send iMessage (macOS only)
def send_imessage(phone_number):
    if not phone_number:
        print("No phone number provided. Message not sent.")
        return
        
    chart_file = generate_chart()
    if not chart_file:
        print("No chart to send. Message not sent.")
        return
    
    message = "Here's your weekly price update! 📊"
    
    try:
        applescript = f'''
        set imagePath to POSIX file "{os.path.abspath(chart_file)}"
        set phoneNumber to "{phone_number}"
        tell application "Messages"
            set theBuddy to buddy phoneNumber of service "SMS"
            send imagePath to theBuddy
            send "{message}" to theBuddy
        end tell
        '''
        
        import platform
        if platform.system() != "Darwin":
            print("iMessage sending is only available on macOS.")
            return
            
        result = subprocess.run(["osascript", "-e", applescript], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Message sent successfully to {phone_number}")
        else:
            print(f"Failed to send message: {result.stderr}")
    except Exception as e:
        print(f"Error sending iMessage: {e}")

# Main function with command line arguments
def main():
    parser = argparse.ArgumentParser(description="Track and report egg and gas prices")
    parser.add_argument("--update", action="store_true", help="Update price data")
    parser.add_argument("--chart", action="store_true", help="Generate price chart")
    parser.add_argument("--send", action="store_true", help="Send chart via iMessage")
    parser.add_argument("--phone", type=str, help="Phone number to send the chart to")
    parser.add_argument("--demo", action="store_true", help="Generate demo data for testing")
    
    args = parser.parse_args()
    
    # Generate demo data if requested
    if args.demo:
        generate_demo_data()
        return
    
    # Default behavior: if no args specified, do everything
    if not (args.update or args.chart or args.send):
        args.update = True
        args.chart = True
    
    # Update data if requested
    if args.update:
        update_data()
    
    # Generate chart if requested
    if args.chart:
        generate_chart()
    
    # Send message if requested
    if args.send:
        phone_number = args.phone
        if not phone_number:
            print("Please provide a phone number with --phone")
            return
        send_imessage(phone_number)

# Function to generate demo data for testing
def generate_demo_data():
    print("Generating demo data for testing...")
    
    # Create a date range for the past 12 weeks
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(weeks=12)
    date_range = pd.date_range(start=start_date, end=end_date, freq='W')
    
    # Generate random price data with a realistic trend
    import numpy as np
    
    # Initial prices
    egg_price_base = 3.25
    gas_price_base = 3.75
    
    # Random walk with some trend
    egg_prices = [egg_price_base]
    gas_prices = [gas_price_base]
    
    for _ in range(1, len(date_range)):
        # Add some randomness and slight upward trend for eggs
        egg_delta = np.random.normal(0.05, 0.15)  # slight upward trend
        new_egg_price = max(1.99, min(5.99, egg_prices[-1] + egg_delta))
        egg_prices.append(round(new_egg_price, 2))
        
        # Add some randomness and slight downward trend for gas
        gas_delta = np.random.normal(-0.03, 0.12)  # slight downward trend
        new_gas_price = max(2.99, min(4.99, gas_prices[-1] + gas_delta))
        gas_prices.append(round(new_gas_price, 2))
    
    # Create DataFrame
    df = pd.DataFrame({
        'date': date_range,
        'egg_price': egg_prices,
        'gas_price': gas_prices
    })
    
    # Save to CSV
    df.to_csv(DATA_FILE, index=False)
    print(f"Demo data saved to {DATA_FILE}")
    
    # Generate chart from demo data
    generate_chart()

if __name__ == "__main__":
    main()