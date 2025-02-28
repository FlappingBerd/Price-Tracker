import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import argparse
import subprocess
from bs4 import BeautifulSoup
import time
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random  # For demo data

# Data file
DATA_FILE = "price_tracker.csv"

class PriceTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Price Tracker")
        self.root.geometry("800x600")
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create buttons
        self.update_button = ttk.Button(self.main_frame, text="Update Prices", command=self.update_prices)
        self.update_button.grid(row=0, column=0, padx=5, pady=5)
        
        # Phone number entry
        self.phone_label = ttk.Label(self.main_frame, text="Phone Number:")
        self.phone_label.grid(row=0, column=1, padx=5, pady=5)
        
        self.phone_entry = ttk.Entry(self.main_frame)
        self.phone_entry.grid(row=0, column=2, padx=5, pady=5)
        
        self.send_button = ttk.Button(self.main_frame, text="Send Graph", command=self.send_graph)
        self.send_button.grid(row=0, column=3, padx=5, pady=5)
        
        # Create demo data button
        self.demo_button = ttk.Button(self.main_frame, text="Generate Demo Data", command=self.generate_demo_data)
        self.demo_button.grid(row=0, column=4, padx=5, pady=5)
        
        # Create figure for matplotlib
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.main_frame)
        self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=5, padx=5, pady=5)
        
        # Price display labels
        self.price_frame = ttk.Frame(self.main_frame)
        self.price_frame.grid(row=2, column=0, columnspan=5, pady=10)
        
        self.egg_price_label = ttk.Label(self.price_frame, text="Current Egg Price: N/A")
        self.egg_price_label.grid(row=0, column=0, padx=20)
        
        self.gas_price_label = ttk.Label(self.price_frame, text="Current Gas Price: N/A")
        self.gas_price_label.grid(row=0, column=1, padx=20)
        
        # Data file path
        self.data_file = "price_tracker.csv"
        
        # Load existing data if available
        self.load_data()

    def fetch_prices(self):
        """Fetch current prices (using random data for demo)"""
        # In reality, you'd implement web scraping here
        egg_price = round(random.uniform(2.50, 4.00), 2)
        gas_price = round(random.uniform(3.00, 4.50), 2)
        return egg_price, gas_price

    def update_prices(self):
        """Update prices and refresh the graph"""
        egg_price, gas_price = self.fetch_prices()
        
        today = datetime.date.today()
        new_data = pd.DataFrame({
            'date': [today],
            'egg_price': [egg_price],
            'gas_price': [gas_price]
        })
        
        if hasattr(self, 'df'):
            self.df = pd.concat([self.df, new_data], ignore_index=True)
        else:
            self.df = new_data
            
        self.df.to_csv(self.data_file, index=False)
        
        # Update labels
        self.egg_price_label.config(text=f"Current Egg Price: ${egg_price:.2f}")
        self.gas_price_label.config(text=f"Current Gas Price: ${gas_price:.2f}")
        
        self.plot_data()
        messagebox.showinfo("Success", "Prices updated successfully!")

    def load_data(self):
        """Load existing data if available"""
        if os.path.exists(self.data_file):
            self.df = pd.read_csv(self.data_file)
            self.df['date'] = pd.to_datetime(self.df['date'])
            self.plot_data()

    def plot_data(self):
        """Plot the price data"""
        self.ax.clear()
        if hasattr(self, 'df'):
            self.df.plot(x='date', y=['egg_price', 'gas_price'], 
                        ax=self.ax, marker='o')
            self.ax.set_title('Price History')
            self.ax.set_xlabel('Date')
            self.ax.set_ylabel('Price ($)')
            self.ax.grid(True)
            self.ax.legend(['Eggs ($/dozen)', 'Gas ($/gallon)'])
            self.fig.autofmt_xdate()  # Angle x-axis labels
            self.canvas.draw()

    def generate_demo_data(self):
        """Generate demo data for testing"""
        dates = pd.date_range(end=datetime.date.today(), periods=30, freq='D')
        self.df = pd.DataFrame({
            'date': dates,
            'egg_price': [round(random.uniform(2.50, 4.00), 2) for _ in range(30)],
            'gas_price': [round(random.uniform(3.00, 4.50), 2) for _ in range(30)]
        })
        self.df.to_csv(self.data_file, index=False)
        self.plot_data()
        
        # Update labels with latest prices
        self.egg_price_label.config(text=f"Current Egg Price: ${self.df['egg_price'].iloc[-1]:.2f}")
        self.gas_price_label.config(text=f"Current Gas Price: ${self.df['gas_price'].iloc[-1]:.2f}")
        
        messagebox.showinfo("Success", "Demo data generated!")

    def send_graph(self):
        """Send the graph to the specified phone number"""
        phone = self.phone_entry.get()
        if not phone:
            messagebox.showerror("Error", "Please enter a phone number!")
            return
            
        # Save current graph
        self.fig.savefig('price_chart.png')
        
        # Here you would implement the actual sending logic
        messagebox.showinfo("Success", f"Graph would be sent to {phone}\n(Sending feature not implemented yet)")

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
    
    # Create a dictionary for the new entry with explicit types
    new_data = pd.DataFrame({
        "date": [pd.to_datetime(today)],
        "egg_price": [egg_price] if egg_price is not None else [pd.NA],
        "gas_price": [gas_price] if gas_price is not None else [pd.NA]
    })
    
    # Load existing data or create new dataframe
    if os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0:
        try:
            df = pd.read_csv(DATA_FILE)
            # Convert date column to datetime
            df["date"] = pd.to_datetime(df["date"])
            # Append new data
            df = pd.concat([df, new_data], ignore_index=True)
        except Exception as e:
            print(f"Error reading existing data file: {e}")
            df = new_data
    else:
        df = new_data
    
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
            # Get the last non-null egg price and its date
            mask = df["egg_price"].notna()
            if mask.any():
                latest_date = df.loc[mask, "date"].iloc[-1]
                latest_egg_price = df.loc[mask, "egg_price"].iloc[-1]
                plt.annotate(f"${latest_egg_price:.2f}",
                             (latest_date.to_pydatetime(), float(latest_egg_price)),
                             textcoords="offset points", 
                             xytext=(0,10),
                             ha='center')
        # Plot gas prices if available
        if "gas_price" in df.columns and not df["gas_price"].isnull().all():
            plt.plot(df["date"], df["gas_price"], label="Gas Price ($/gallon)", marker="s", color="blue")
            # Annotate latest gas price
            mask = df["gas_price"].notna()
            if mask.any():
                latest_date = df.loc[mask, "date"].iloc[-1]
                latest_gas_price = df.loc[mask, "gas_price"].iloc[-1]
                plt.annotate(f"${latest_gas_price:.2f}",
                             (latest_date.to_pydatetime(), float(latest_gas_price)),
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
    from numpy.random import normal
    
    # Initial prices
    egg_price_base = 3.25
    gas_price_base = 3.75
    
    # Random walk with some trend
    egg_prices = [egg_price_base]
    gas_prices = [gas_price_base]
    
    for _ in range(1, len(date_range)):
        # Add some randomness and slight upward trend for eggs
        egg_delta = normal(0.05, 0.15)  # slight upward trend
        new_egg_price = max(1.99, min(5.99, egg_prices[-1] + egg_delta))
        egg_prices.append(round(new_egg_price, 2))
        # Add some randomness and slight downward trend for gas
        gas_delta = normal(-0.03, 0.12)  # slight downward trend
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
    root = tk.Tk()
    app = PriceTrackerApp(root)
    root.mainloop()