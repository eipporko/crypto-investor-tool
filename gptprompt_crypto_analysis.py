import requests
import argparse
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from openai import OpenAI

# Parse command line arguments
parser = argparse.ArgumentParser(description='Analyzes the cryptocurrency market using ChatGPT based on given inputs.')
parser.add_argument('--gpt_token', type=str, required=True, help='The access token for OpenAI GPT. This token is required to make API requests.')
parser.add_argument('--language', type=str, help='The language in which the analysis should be performed. Defaults to "English" if not specified.', default='english')
args = parser.parse_args()

# Function definition to fetch historical data
def fetch_historical_data_with_volume(from_timestamp, to_timestamp):
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart/range"
    params = {
        'vs_currency': 'usd',
        'from': from_timestamp,
        'to': to_timestamp
    }
    response = requests.get(url, params=params)
    data = response.json()
    prices = data['prices']
    volumes = data['total_volumes']
    df = pd.DataFrame(prices, columns=['timestamp', 'price'])
    df_volume = pd.DataFrame(volumes, columns=['timestamp', 'volume'])
    df['volume'] = df_volume['volume']
    df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('date', inplace=True)
    return df




# Function definition to calculate the MA and the multiplier
def calculate_2y_ma_multiplier(df):
    # Assuming 365 days per year, so 730 represents roughly 2 years
    df['MA_2y'] = df['price'].rolling(window=730, min_periods=1).mean()
    df['MA_2y_multiplier'] = df['MA_2y'] * 5
    return df



# Function to fetch the Fear and Greed Index
def fetch_fear_and_greed_index(days):
    api_url = "https://api.alternative.me/fng/"
    response = requests.get(f"{api_url}?limit={days}")
    data = response.json()
    index_data = data.get('data', [])
    df = pd.DataFrame(index_data)
    df['timestamp'] = pd.to_numeric(df['timestamp'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s').dt.strftime('%Y-%m-%d')
    df.rename(columns={'value': 'fear_and_greed_index'}, inplace=True)
    df.set_index('timestamp', inplace=True)
    return df



# Function to fetch current crypto data
def fetch_crypto_data(date):
    dt_object = datetime.utcfromtimestamp(int(date.timestamp()))
    date = dt_object.strftime('%d-%m-%Y')
    url = 'https://api.coingecko.com/api/v3/coins/bitcoin/history'
    params = {
        'date': date
    }
    response = requests.get(url, params=params)
    data = response.json()

    results = {
        'price': data["market_data"]["current_price"]["usd"],
        'volume': data["market_data"]["total_volume"]["usd"]
    }
    return results



def calculate_average_volume_last_date(df, days):
    df_sorted = df.sort_index()

    last_date = df_sorted.index[-1]
    
    start_date = last_date - timedelta(days=30)
    
    df_filtered = df_sorted.loc[start_date:last_date]
    
    average_volume = df_filtered['volume'].mean()
    
    return average_volume



def get_analysis_data(df, current_data):
    last_row = df.iloc[-1]
    ma_2y = last_row['MA_2y']
    ma_2y_multiplier = last_row['MA_2y_multiplier']
    volume_mean = calculate_average_volume_last_date(df, 30)
    fear_and_greed_index = fetch_fear_and_greed_index(1).iloc[-1]['fear_and_greed_index']

    diff_ma_2y = current_data['price'] - ma_2y
    diff_ma_2y_percent = (diff_ma_2y / ma_2y) * 100
    diff_ma_2y_multiplier = current_data['price'] - ma_2y_multiplier
    diff_ma_2y_multiplier_percent = (diff_ma_2y_multiplier / ma_2y_multiplier) * 100
    diff_volume = current_data['volume'] - volume_mean
    diff_volume_percent = ( diff_volume / volume_mean ) * 100
    
    results = {
        'current_price': current_data['price'],
        'current_volume': current_data['volume'],
        'volume_mean_last_30_days': volume_mean,
        'ma_2y': ma_2y,
        'ma_2y_multiplier': ma_2y_multiplier,
        'diff_ma_2y': diff_ma_2y,
        'diff_ma_2y_percent': diff_ma_2y_percent,
        'diff_ma_2y_multiplier': diff_ma_2y_multiplier,
        'diff_ma_2y_multiplier_percent': diff_ma_2y_multiplier_percent,
        'diff_volume': diff_volume,
        'diff_volume_percent': diff_volume_percent,
        'fear_and_greed_index': fear_and_greed_index
    }
    
    return results



def analyze_crypto_market(api_key, analysis_data, language='English'):

    client = OpenAI(
        # This is the default and can be omitted
        api_key=api_key
    )

    # Formato de los datos para el prompt
    description = "You are an AI trained to analyze the cryptocurrency market and recommend actions based on specific market data and indicators."
    user_input = (
        f"Based on the analysis of the cryptocurrency market with the following data: "
        f"Current price of Bitcoin is ${analysis_data['current_price']:.2f}, "
        f"the price is {analysis_data['diff_ma_2y_percent']:.2f}% {'above' if analysis_data['diff_ma_2y_percent'] > 0 else 'below'} "
        f"the 2-year moving average, "
        f"the price is {analysis_data['diff_ma_2y_multiplier_percent']:.2f}% {'above' if analysis_data['diff_ma_2y_multiplier_percent'] > 0 else 'below'} "
        f"the 2-year moving average multiplied by 5, "
        f"the trading volume has changed by {analysis_data['diff_volume_percent']:.2f}% compared to the 30-day average, "
        f"and the Fear and Greed Index is at {analysis_data.get('fear_and_greed_index', 'not provided')}. "
        f"Given this data, provide a concise analysis for both a conservative, long-term investment strategy and an aggressive, short-term investment strategy. "
        f"If you mention any index, please specify its value. "
        f"Conclude each strategy's analysis with a headline summarizing your recommendation. "
        f"Please aim for a maximum of 20 words per strategy."
        f"Please provide the analysis in {language}."
    )




    messages = [
        {"role": "system", "content": "You are an AI trained to analyze the cryptocurrency market and recommend actions based on specific market data and indicators."},
        {"role": "user", "content": user_input}
    ]

    try:
        # Realiza la consulta a la API de OpenAI utilizando el formato de ChatCompletion
        completion = client.chat.completions.create(
            messages = messages,
             model = "gpt-4",
        )


    except openai.error.OpenAIError as e:
        # Maneja posibles errores con la API
        completion = f"OpenAI API error: {e}"

    return completion.choices[0].message.content





# Assuming you want to fetch data from the beginning of Bitcoin trading on CoinGecko
from_date = datetime(2013, 4, 28)
from_timestamp = int(from_date.timestamp())
to_date = datetime.now()
to_timestamp = int(to_date.timestamp())

# Fetch historical Bitcoin data
df = fetch_historical_data_with_volume(from_timestamp, to_timestamp)

# Calculate the 2-year MA and its multiplier
df_ma = calculate_2y_ma_multiplier(df)

current_price = fetch_crypto_data(to_date)
analysis_data = get_analysis_data(df_ma, current_price)

recomendation = analyze_crypto_market(args.gpt_token, analysis_data, args.language)

print(recomendation)