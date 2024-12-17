import pandas as pd
import yfinance as yf
from datetime import datetime

COMMODITY_ETFS = {
    'Industrial_Metals': 'JJM',
    'Base_Metals': 'DBB',
    'Metals_and_Mining': 'XME',
}

MATERIALS_INDEXES = {
    'Materials': 'XLB',
    'Basic_Materials': 'VAW',
}

AEROSPACE_INDEXES = {
    'Aerospace': 'ITA',
    'Defense': 'PPA',
    'Spider_Defense': 'XAR',
}

FUTURES = {
    'Aluminum': 'ALI=F',
}

TIER_FOUR = {}

TIER_THREE = {
    'Luna_Innovations': 'LUNA',
    'Lightpath_Technologies': 'LPTH',
    'Kale_Aero': 'KIPA.IS',
    'Materion_Corporation': 'MTRN',
    'Kitron_ASA': 'KIT.OL',
    'Ducommun_Labarge': 'DCO',
    'Carpenter_Technology': 'CRS',
    'Quickstep_Holdings': 'QHL.AX',
    'GKN_Aerospace': 'MRO.L',
    'Dupont': 'DD',
    'Hardide': 'HDD.L',
}

TIER_TWO = {}

TIER_ONE = {}

CONTROLS = {
    'SP500': 'SPY',              
    'General_Commodities': 'DBC', 
    'Industrial_Sector': 'XLI',   
    'Russell_2000': 'IWM',       
}

TICKERS = {
    **COMMODITY_ETFS,
    **MATERIALS_INDEXES,
    **AEROSPACE_INDEXES,
    **FUTURES,
    **TIER_ONE,
    **TIER_TWO,
    **TIER_THREE,
    **TIER_FOUR,
    **CONTROLS
}

def validate_format(contract_date_str):
    """Validate that the date string is in MM/DD/YYYY format."""
    try:
        datetime.strptime(contract_date_str, "%m/%d/%Y")
    except ValueError:
        raise ValueError(f"{contract_date_str} not in correct MM/DD/YYYY format")

def collect_market_data(contract_date_str):
    """
    Collect market data with guaranteed timezone consistency and save to CSV files.
    """
    contract_date = pd.to_datetime(contract_date_str)
    end_date = contract_date + pd.Timedelta(days=5)
    start_date = end_date - pd.Timedelta(days=120)

    validate_format(contract_date_str)
    
    data_dict = {}
    volume_dict = {}
    
    for name, ticker in TICKERS.items():
        try:
            stock = yf.Ticker(ticker)
            # Force UTC timezone during download
            hist = stock.history(start=start_date, end=end_date, interval='1d')
            
            # Convert to naive datetime immediately after download
            if hasattr(hist.index, 'tz'):
                hist.index = hist.index.tz_localize(None)
            
            # Store the data
            data_dict[name] = hist['Close'].round(2)
            volume_dict[name] = hist['Volume']
            print(f"Downloaded {name} data")
            
        except Exception as e:
            print(f"Error downloading {name}: {str(e)}")
            continue
    
    # Create DataFrames with index handling
    market_history = pd.DataFrame(data_dict)
    volume_history = pd.DataFrame(volume_dict)

    if market_history.empty or volume_history.empty:
        print("Warning: No data was collected for one or more assets")
        if market_history.empty:
            print("Market price data is empty")
        if volume_history.empty:
            print("Volume data is empty")
    
    # Ensure index consistency 
    if not market_history.empty:
        if hasattr(market_history.index, 'tz'):
            market_history.index = pd.DatetimeIndex([idx.tz_localize(None) for idx in market_history.index])
    
    if not volume_history.empty:
        if hasattr(volume_history.index, 'tz'):
            volume_history.index = pd.DatetimeIndex([idx.tz_localize(None) for idx in volume_history.index])
    
    # Format the contract date into YYYYMMDD for clean filenames
    contract_date_formatted = pd.to_datetime(contract_date_str).strftime('%Y%m%d')
    
    # Create descriptive filenames that include the data type and contract date
    prices_filename = f'market_prices_{contract_date_formatted}.csv'
    volumes_filename = f'market_volumes_{contract_date_formatted}.csv'
    
    try:
        # Save the market prices DataFrame to CSV
        market_history.to_csv(prices_filename)
        print(f"Successfully saved market prices to {prices_filename}")
        
        # Save the trading volumes DataFrame to CSV
        volume_history.to_csv(volumes_filename)
        print(f"Successfully saved trading volumes to {volumes_filename}")
        
    except Exception as e:
        # Provide helpful error information if saving fails
        print(f"Error saving CSV files: {str(e)}")
        print("Data was collected but could not be saved to files")

    return market_history, volume_history
