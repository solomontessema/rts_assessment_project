from sec_edgar_downloader import Downloader
import os

def fetch_sec_filings(ticker: str):
    """Downloads the latest 10-K (Annual Report) for a given ticker."""
    # Initialize the downloader with your info (SEC requirement)
    dl = Downloader("SolomonProject", "solomon.tessema@outlook.com")
    
    # Download the 10-K to a folder named 'sec-edgar-filings'
    # 'after' ensures we get recent data
    dl.get("10-K", ticker, after="2023-01-01", download_details=False)
    
    return f"Successfully downloaded the latest 10-K for {ticker}."

# Test it out (e.g., Apple Inc.)
# print(fetch_sec_filings("AAPL"))