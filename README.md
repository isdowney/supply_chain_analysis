# F-35 Supply Chain Analysis Project

## Overview
A comprehensive Python-based analysis system that maps and analyzes the F-35 fighter jet's supply chain through financial market data. The project combines supply chain mapping, market data analysis, and statistical modeling to understand relationships and patterns across different supply chain tiers.

## Features
- Multi-tier supply chain mapping (4 tiers deep) of the F-35 program
- Real-time market data collection and analysis
- Advanced statistical analysis of price trends and volume patterns
- Cross-tier correlation analysis
- Supply chain preparation activity detection
- Composite signal generation for supply chain insights

## Technical Architecture

### Core Components
1. **Supply Chain Mapping** (`supply_chain.py`)
   - Database management for supplier information
   - Tier-based classification system
   - Supplier validation and update functionality
   - Comprehensive supplier metadata tracking

2. **Market Data Collection** (`data_collector.py`)
   - Integration with yfinance API
   - Automated data collection for multiple asset classes
   - Handling of international securities and ETFs
   - Robust error handling and data validation

3. **Market Analysis** (`market_analysis.py`)
   - Statistical trend analysis with multiple time windows
   - Volume pattern analysis using z-score methodology
   - Cross-tier correlation analysis
   - Composite signal generation
   - Statistical validation against market controls

## Technologies Used
- **Python**: Primary programming language
- **Key Libraries**:
  - pandas: Data manipulation and analysis
  - numpy: Numerical computations
  - scipy: Statistical analysis
  - yfinance: Market data collection
  
## Data Sources
- Stock market data for public companies
- ETF data for sector analysis
- Commodity futures data
- Market indices for control comparisons

## Analysis Capabilities

### Market Analysis Features
- Price trend detection across multiple time windows (4, 8, 12 weeks)
- Volume pattern analysis with statistical validation
- Supply chain correlation mapping
- Composite signal generation combining multiple indicators
- Control-adjusted statistical validation

### Statistical Methods
- Mann-Whitney U tests for trend validation
- Z-score analysis for volume patterns
- Rolling correlation analysis
- Multiple control group comparisons
- Statistical significance testing

## Project Structure
```
project/
├── supply_chain.py      # Supply chain database management
├── data_collector.py    # Market data collection system
├── market_analysis.py   # Statistical analysis engine
├── f35_suppliers.csv    # Master supplier database
└── analysis_results/    # Output directory for analysis results
    ├── market_data_*.csv        # Historical price data
    ├── market_prices_*.csv      # Processed daily closing prices
    ├── market_volumes_*.csv     # Raw trading volume data
    ├── volume_data_*.csv        # Processed volume analysis
    ├── volume_patterns_*.csv    # Unusual volume pattern analysis
    ├── correlations_*.csv       # Cross-tier correlation results
    ├── price_trends_*.csv       # Identified price trends and validations
    └── composite_signals_*.csv  # Combined analysis signals
```

## Future Enhancements
- Integration of machine learning models for pattern recognition
- Real-time alert system for significant supply chain events
- Enhanced visualization capabilities
- API development for external system integration

## Usage
1. Initialize supply chain database:
```python
python supply_chain.py
```

2. Collect market data:
```python
from data_collector import collect_market_data
market_data, volume_data = collect_market_data("MM/DD/YYYY")
```

3. Run analysis:
```python
from market_analysis import analyze_contract_preparation
results = analyze_contract_preparation("MM/DD/YYYY")
```

## Contributing
This project is currently maintained as part of a portfolio demonstration. Contributions and suggestions are welcome through the issues system.
