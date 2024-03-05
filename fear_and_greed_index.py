import requests
import pandas as pd
import argparse

# Define the API endpoint
api_url = "https://api.alternative.me/fng/"

# Specify the number of days for historical data
days = 10  # For example, last 10 days. Adjust as needed.

# Make a GET request to fetch the Fear and Greed Index data
response = requests.get(f"{api_url}?limit={days}")
data = response.json()

# Extract the 'data' portion from the response
index_data = data.get('data', [])

# Convert the data to a pandas DataFrame for better visualization and analysis
df = pd.DataFrame(index_data)

# Convert timestamp to readable date format
df['timestamp'] = pd.to_numeric(df['timestamp'])
df['time_until_update'] = pd.to_numeric(df['time_until_update'])

df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s').dt.strftime('%Y-%m-%d')
df['time_until_update'] = pd.to_datetime(df['time_until_update'], unit='s').dt.strftime('%H:%M:%S')

print(df)
