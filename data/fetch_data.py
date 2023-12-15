import yfinance as yf

def fetch_crypto_data(start_date, end_date, price_col,ticker = "BTC-USD"): 
    bitcoin_data = yf.download(ticker, start=start_date, end=end_date)
    return bitcoin_data[price_col]