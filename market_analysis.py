import pandas as pd
import numpy as np
import scipy.stats as stats
from data_collector import collect_market_data

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

def analyze_price_trends(market_data, window_sizes=[4, 8, 12], threshold=0.05):
    """
    Analyze sustained price trends over different time windows
    by looking for consistent price movements that might indicate
    meaningful market trends rather than just noise.
    """

    print("Starting analysis with data shape:", market_data.shape)    #NEW
    print("Data date range:", market_data.index.min(), "to", market_data.index.max())    #NEW
    trend_analysis = {}
    
    for ticker in market_data.columns:
        print(f"Processing ticker: {ticker}")    #NEW
        try:
            ticker_data = market_data[ticker].fillna(method='ffill')
            print(f"Ticker data shape: {ticker_data.shape}")    #NEW
            trends = {}
            
            for window in window_sizes:
                # Convert window from weeks to trading days
                window_days = window * 5  # Assuming 5 trading days per week
                print(f"Processing window size: {window} weeks ({window_days} days)")  #NEW
                
                # Calculate rolling mean
                rolling_mean = ticker_data.rolling(window=window_days).mean()
                
                # Calculate growth rates between periods
                growth_rates = (rolling_mean - rolling_mean.shift(window_days)) / rolling_mean.shift(window_days)

                market_returns = (market_data['SP500'].rolling(window=window_days, min_periods=3).mean() - \
                    market_data['SP500'].rolling(window=window_days, min_periods=3).mean().shift(window_days)) / \
                    market_data['SP500'].rolling(window=window_days, min_periods=3).mean().shift(window_days)
                sector_returns = (market_data['Industrial_Sector'].rolling(window=window_days, min_periods=3).mean() - \
                    market_data['Industrial_Sector'].rolling(window=window_days, min_periods=3).mean().shift(window_days)) / \
                    market_data['Industrial_Sector'].rolling(window=window_days, min_periods=3).mean().shift(window_days)

                # Adjust growth rates
                adjusted_growth_rates = growth_rates - (market_returns + sector_returns)/2
                
                # Find periods of sustained growth above threshold
                significant_trends = adjusted_growth_rates[adjusted_growth_rates > threshold]
                print(f"Found {len(significant_trends)} significant trends")  #NEW
                
                if len(significant_trends) > 0:
                    print(f"Creating trends dictionary for window {window}")  #NEW
                    trends[f'{window}w'] = {
                        'start_dates': significant_trends.index.tolist(),
                        'growth_rates': significant_trends.values.tolist()
                    }
                    print(f"Successfully added trends for window {window}")  #NEW
            
            if trends:  
                trend_analysis[ticker] = trends
                
        except Exception as e:
            print(f"Warning: Could not analyze trends for {ticker}: {str(e)}")
            continue

    validation_results = _validate_market_patterns(
        market_data, 
        trend_analysis, 
    )

    for ticker in trend_analysis:
        if ticker in validation_results:
            trend_analysis[ticker]['statistical_validation'] = validation_results[ticker]
    
    return trend_analysis

def _validate_market_patterns(data, patterns, significance_level=0.05):
    """
    Helper function to statistically validate identified market patterns.
    
    Parameters:
        data: pd.DataFrame - The market data being analyzed
        patterns: dict - The patterns identified by main analysis functions
        pattern_type: str - Type of pattern being validated ('price', 'volume', 'correlation')
        significance_level: float - P-value threshold for statistical significance
        
    Returns:
        dict - Statistical validation results for each pattern
    """
    validation_results = {}
    
    # Add control data
    control_data = {
        'market': data['SP500'].pct_change().dropna(),
        'sector': data['Industrial_Sector'].pct_change().dropna(),
        'commodities': data['General_Commodities'].pct_change().dropna(),
        'small_cap': data['Russell_2000'].pct_change().dropna()
    }
    
    for ticker, trends in patterns.items():
        print(f"\nValidating {ticker} with trends:", trends)
        ticker_data = data[ticker].pct_change().dropna()
        
        # Keep the working trend periods code
        trend_periods = pd.Series(False, index=ticker_data.index)
        print(f"Created trend_periods with index:", trend_periods.index[:5], "...")
        
        for window_data in trends.values():
            print(f"Processing window data:", window_data)
            if '4w' in window_data:
                for start_date in window_data['4w']['start_dates']:
                    trend_periods[start_date] = True
            if '8w' in window_data:
                for start_date in window_data['8w']['start_dates']:
                    trend_periods[start_date] = True

        # Add control comparison
        if trend_periods.any() and (~trend_periods).any():
            # Calculate regular statistic
            statistic, base_p_value = stats.mannwhitneyu(
                ticker_data[trend_periods],
                ticker_data[~trend_periods],
                alternative='greater'
            )
            
            # Calculate control-adjusted statistics
            control_stats = {}
            for control_name, control_series in control_data.items():
                adjusted_returns = ticker_data - control_series
                stat, p_value = stats.mannwhitneyu(
                    adjusted_returns[trend_periods],
                    adjusted_returns[~trend_periods],
                    alternative='greater'
                )
                control_stats[control_name] = p_value
            
            # Only significant if beats base test and all controls
            validation_results[ticker] = {
                'p_value': base_p_value,
                'control_p_values': control_stats,
                'significant': base_p_value < significance_level and all(p < significance_level for p in control_stats.values()),
                'confidence': 1 - max([base_p_value] + list(control_stats.values()))
            }
    
    return validation_results

def analyze_volume_patterns(volume_data, z_score_threshold=2):
    """
    Identify periods of unusually high trading volume that might indicate
    supply chain preparation activity.
    """
    volume_signals = {}
    
    for ticker in volume_data.columns:
        # Calculate rolling mean and standard deviation of volume
        rolling_mean = volume_data[ticker].rolling(window=20).mean()
        rolling_std = volume_data[ticker].rolling(window=20).std()
        
        # Calculate volume Z-scores
        z_scores = (volume_data[ticker] - rolling_mean) / rolling_std
        
        # Find periods of unusual volume
        unusual_volume = z_scores[z_scores > z_score_threshold]
        
        if len(unusual_volume) > 0:
            volume_signals[ticker] = {
                'dates': unusual_volume.index.tolist(),
                'z_scores': unusual_volume.values.tolist()
            }
    
    return volume_signals

def analyze_supply_chain_correlation(market_data, window_size=20):
    """
    Analyze correlations between different parts of the supply chain.
    Returns dictionary of mean correlations between pairs of assets.
    """
    # Initialize results dictionary
    correlations = {}
    
    # Convert market data index to datetime 
    market_data.index = pd.to_datetime(market_data.index)
    
    valid_tickers = [
        ticker for ticker in market_data.columns
        if (ticker in ['Metals', 'Materials'] or 
            ticker in TIER_THREE or 
            any(x in ticker for x in ['ETF', 'Materials', 'Aerospace']))
    ]
    
    for i, t1 in enumerate(valid_tickers):
        for t2 in valid_tickers[i+1:]:
            try:
                # Get price series for both assets
                series1 = market_data[t1]
                series2 = market_data[t2]
                
                # Calculate returns, handling missing values properly
                returns1 = np.log(series1 / series1.shift(1)).replace([np.inf, -np.inf], np.nan).fillna(0)
                returns2 = np.log(series2 / series2.shift(1)).replace([np.inf, -np.inf], np.nan).fillna(0)
                
                # Create DataFrame of returns for correlation calculation
                returns_df = pd.DataFrame({
                    t1: returns1,
                    t2: returns2
                }, index=market_data.index)
                
                # Calculate rolling correlation 
                roll_corr = returns_df[t1].rolling(
                    window=window_size,
                    min_periods=5  
                ).corr(returns_df[t2])
                
                # Store correlation series with its index intact
                key = f'{t1}_{t2}'
                correlations[key] = roll_corr
                
            except Exception as e:
                print(f"Warning: Could not calculate correlation for {t1}-{t2}: {str(e)}")
                continue
    
    return correlations

def create_composite_signals(market_data, contract_dates, volume_patterns, correlations):
    """
    Create composite signals by combining volume patterns and correlations.
    """
    # Initialize signals dictionary
    signals = {}
    
    # Process each contract date separately
    for contract_date in pd.to_datetime(contract_dates):
        # Initialize daily scores for this contract date
        daily_scores = pd.Series(0.0, index=market_data.index)
        
        # Add volume pattern signals
        if volume_patterns:
            for ticker, vol_data in volume_patterns.items():
                signal_dates = pd.to_datetime(vol_data['dates'])
                
                # Add normalized volume signals
                for date, score in zip(signal_dates, vol_data['z_scores']):
                    if date in daily_scores.index:
                        # Use a fixed scaling factor instead of len(volume_patterns)
                        daily_scores.at[date] += float(score) / 10.0  # Scale to reasonable range
        
        # Add correlation signals
        if correlations:
            for group_pair, corr_series in correlations.items():
                # Convert to numeric and handle any missing values
                corr_series = pd.to_numeric(corr_series, errors='coerce')
                
                # Add scaled correlation values
                daily_scores += corr_series.abs().fillna(0) / 5.0  # Scale to reasonable range
        
        # Store the composite signal for this contract date
        signals[contract_date] = daily_scores
    
    return signals

def analyze_contract_preparation(contract_date_str, output_dir='analysis_results'):
    """
    Coordinate all sub-analyses and saves results to CSV files.
    """
    try:
        print(f"\nStarting analysis for {contract_date_str}")
        
        # Create output directory if it doesn't exist
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        # Format date once and store for reuse
        analysis_date = pd.to_datetime(contract_date_str)
        date_for_filename = analysis_date.strftime('%Y%m%d')
        
        # Collect and validate market data
        market_data, volume_data = collect_market_data(contract_date_str)
        if market_data is None or volume_data is None:
            raise ValueError(f"Market data collection failed for date {contract_date_str}")
        
        # Perform analyses with validation
        volume_patterns = analyze_volume_patterns(volume_data)  
        if volume_patterns is None:
            print("Warning: Volume pattern analysis produced no results")
            volume_patterns = {}
            
        correlations = analyze_supply_chain_correlation(market_data)
        if correlations is None:
            print("Warning: Correlation analysis produced no results")
            correlations = {}
            
        price_trends = analyze_price_trends(market_data)
        if price_trends is None:
            print("Warning: Price trend analysis produced no results")
            price_trends = {}
        
        # Create composite signals with validated parameters
        signals = create_composite_signals(
            market_data=market_data,
            contract_dates=[analysis_date],
            volume_patterns=volume_patterns,
            correlations=correlations
        )
        
        # Save results in an organized way
        def save_data(data, filename, index=True):
            full_path = os.path.join(output_dir, f'{filename}_{date_for_filename}.csv')
            if isinstance(data, pd.DataFrame):
                data.to_csv(full_path, index=index)
            elif isinstance(data, dict):
                pd.DataFrame.from_dict(data, orient='index').to_csv(full_path)
            print(f"Saved {filename} to {full_path}")
        
        # Save all results using consistent method
        save_data(market_data, 'market_data')
        save_data(volume_data, 'volume_data')
        
        if volume_patterns:
            save_data(volume_patterns, 'volume_patterns')
        if correlations:
            save_data(correlations, 'correlations')
            
        if price_trends:
            trend_rows = [
                {
                    'ticker': ticker,
                    'window': window,
                    'start_date': start_date,
                    'growth_rate': growth_rate
                }
                for ticker, trends in price_trends.items()
                for window, data in trends.items()
                for start_date, growth_rate in zip(data['start_dates'], data['growth_rates'])
            ]
            if trend_rows:
                save_data(pd.DataFrame(trend_rows), 'price_trends', index=False)
                
        if signals is not None:
            save_data(signals, 'composite_signals')
        
        # Create and save summary report
        analysis_report = {
            'volume_signals': volume_patterns,
            'correlations': correlations,
            'price_trends': price_trends,
            'composite_signals': signals[analysis_date] if signals else None
        }
        
        return analysis_report
        
    except Exception as e:
        print(f"Error in analyze_contract_preparation: {str(e)}")
        return None
    
analyze_contract_preparation("04/28/2017")