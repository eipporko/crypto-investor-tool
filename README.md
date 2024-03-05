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

## Conclusion

Leverage these scripts for strategic insights into the cryptocurrency market. Ensure adherence to API data usage rules.