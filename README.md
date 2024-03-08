# Cryptocurrency Analysis Tools

Explore the cryptocurrency market with a suite of Python scripts, including visualizations of Crypto's 2-Year MA Multiplier Chart, real-time market insights, and sentiment analysis through the Fear and Greed Index. These tools provide a comprehensive look at market trends, performance, and sentiment.

---

## 2-Year MA Multiplier Chart Script

Visualize Crypto's price against its 2-Year Moving Average and a 5x multiplier. This graph aids in identifying market cycles, highlighting periods of potential under or overvaluation.

### Installation and Usage

Dependencies: `requests`, `pandas`, `matplotlib`, `mplcursors`. Install via pip:

```bash
pip install requests pandas matplotlib mplcursors
```

To run:

```bash
python crypto_market_cycle_visualizer.py bitcoin --currency usd --include_halvings --from_date "2018-01-01" --to_date "2024-03-05"
```

### Insights from the Chart

- **Crypto Price**: Shows daily crypto pricing.
- **2-Year MA and 2-Year MA x5**: Indicate long-term trends and potential overvaluation zones.
- **Green and Red Shaded Areas**: Highlight undervaluation (buy) and overvaluation (sell) periods respectively.

### Credits

Inspired by "Bitcoin Investor Tool: 2-Year MA Multiplier" from [LookIntoBitcoin](https://www.lookintobitcoin.com/charts/bitcoin-investor-tool/).

---

## Crypto Market Insight Script

Fetches current values, 24-hour volumes, and their percentage changes for specified cryptocurrencies.

### Usage

For specific cryptos and currency code:

```bash
python crypto_market_insight.py bitcoin ethereum --currency eur
```

To list all CoinGecko IDs:

```bash
python crypto_market_insight.py --list
```

---

## Fear and Greed Index Script

Accesses the Fear and Greed Index to snapshot the market sentiment.

### Usage

To fetch the latest or historical index values:

```bash
python fear_and_greed_index.py
```

---

## GPT Prompt Bitcoin Analysis Script

Utilize the power of GPT (Generative Pre-trained Transformer) for in-depth analysis of the Bitcoin market. This script fetches historical data, calculates the 2-Year Moving Average (MA) and its multiplier, fetches the current Bitcoin data, and uses GPT to analyze and provide recommendations for both conservative and aggressive investment strategies based on current market conditions.

### Installation and Usage

Dependencies: `requests`, `pandas`, `numpy`, `datetime`, `openai`. Ensure you have installed the previous dependencies listed for other scripts and then install the OpenAI library via pip:

```bash
pip install openai
```

Before running the script, you need an OpenAI API key. Please visit [OpenAI](https://openai.com/api/) to obtain your API key.

To run:

```bash
python gptprompt_market_analysis.py --gpt_token YOUR_OPENAI_API_TOKEN
```

Additional arguments include `--language` to specify the analysis's language, defaulting to English if not provided.

### Features of the Script

- **Fetches Historical Data**: Collects historical pricing and volume data for Bitcoin.
- **Calculates MA and Multiplier**: Computes the 2-Year MA and its 5x multiplier for trend analysis.
- **GPT-Driven Analysis**: Leverages GPT for market analysis and investment strategy recommendations.
- **Supports Multiple Languages**: Capable of providing analysis in different languages.

### Insights Provided

- **Market Trends**: Understand current market trends compared to historical averages.
- **Investment Strategies**: Receive tailored investment strategies based on advanced AI analysis.
- **Volume Analysis**: Analyzes changes in trading volume against a 30-day average.
- **Fear and Greed Index**: Incorporates the Fear and Greed Index for sentiment analysis.

### Credits

This script was developed to integrate advanced AI analysis into cryptocurrency market strategies. The usage of OpenAI's GPT for financial analysis represents a pioneering approach to investment strategy recommendations.

---

## Conclusion

Leverage these scripts for strategic insights into the cryptocurrency market. Ensure adherence to API data usage rules.