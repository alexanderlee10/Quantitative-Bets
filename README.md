# 🏈 Quantitative Bets - Sports Analytics Platform

A comprehensive sports betting analysis platform that combines real-time data scraping, statistical modeling, and interactive dashboards to help make informed sports betting decisions.

## 🎯 **What This Does**

### **Smart Sports Analysis**
- **Real-time Data**: Live scraping from StatMuse with reliable fallbacks
- **Statistical Modeling**: Weighted Moving Averages, Probability Calculations, Confidence Intervals
- **Multi-Sport Coverage**: NBA, NFL, NHL, WNBA with unified analysis
- **Risk Assessment**: Probability calculations and betting recommendations

### **Technical Features**
- **Modular Design**: Clean, organized code that's easy to extend
- **Data Pipeline**: Robust scraping with error handling and sample data fallbacks
- **Interactive Dashboard**: Real-time visualizations with dark theme
- **Performance Optimized**: Efficient algorithms for quick analysis

## 🚀 **Quick Start**

### **One-Command Launch**
```bash
python quick_start.py
```

### **Manual Installation**
```bash
git clone https://github.com/yourusername/Quantitative-Bets.git
cd Quantitative-Bets
pip install -r requirements.txt
cd src/dashboards
python multi_sport_dashboard.py
```

## 🏗️ **Project Structure**

```
Quantitative-Bets/
├── quick_start.py                   # One-click launcher
├── setup.py                         # Package distribution
├── requirements.txt                 # Dependencies
├── README.md                        # Documentation
├── src/                             # Core application
│   ├── core/                        # Sport-specific data processing
│   │   ├── NBBBA.py                # NBA analytics engine
│   │   ├── nhl.py                  # NHL data processor
│   │   └── MLB.py                  # MLB integration
│   ├── scrapers/                    # Real-time data acquisition
│   │   ├── datascrapper.py         # Primary data scraper
│   │   ├── teamstatscraper.py      # Team statistics engine
│   │   └── team_defense_scraper.py # Defense analysis module
│   ├── analyzers/                   # Statistical analysis engine
│   │   ├── simplemean.py           # Basic statistical functions
│   │   ├── WMA.py                  # Weighted Moving Average
│   │   ├── combined_stats_analyzer.py # Advanced analytics
│   │   └── comprehensive_defense_analyzer.py # Defense metrics
│   ├── dashboards/                  # User interface layer
│   │   └── multi_sport_dashboard.py # Primary dashboard
│   └── utils/                       # Utility functions
│       ├── plot.py                  # Visualization utilities
│       └── enhanced_plot.py        # Advanced plotting
├── tests/                           # Test files
├── examples/                        # Usage examples
└── docs/                           # Documentation
```

## 📊 **Analytics Features**

### **Multi-Sport Statistical Engine**
- **NBA**: Complete player statistics with team defense analysis
- **NFL**: Quarterback and player performance metrics
- **NHL**: Player scoring and assist tracking
- **WNBA**: Women's basketball statistics

### **Real-Time Data Processing**
- **Live Scraping**: StatMuse integration with retry mechanisms
- **Data Validation**: Error checking and data integrity
- **Fallback Data**: Sample data when live sources unavailable
- **Caching**: Optimized performance with smart data storage

### **Statistical Modeling**
- **Weighted Moving Average (WMA)**: Trend-weighted analysis for better predictions
- **Combined Statistics**: PRA, PR, PA, RA and custom combinations
- **Probability Calculations**: CDF, PDF, and hit probability analysis
- **Confidence Intervals**: Statistical reliability measures
- **Risk Assessment**: Betting recommendations based on data

## 🎨 **Dashboard Interface**

### **Interactive Features**
- **Color-coded Performance**: Visual hit/miss indicators (green/red)
- **Real-time Updates**: Live data integration
- **Responsive Design**: Works on different screen sizes
- **Dark Theme**: Easy on the eyes for long sessions

### **Analytics Dashboard**
- **Performance Charts**: Bar graphs with trend lines and projections
- **Team Defense Rankings**: Opponent difficulty analysis
- **Statistical Analysis**: Normal distribution with probability curves
- **Opponent Analysis**: Detailed matchup breakdown
- **Hit Probability**: Percentage chance of hitting projection
- **Recommendations**: Strong/Moderate/Avoid bet suggestions

### **Dashboard Screenshots**

#### **Initial Dashboard State**
![Dashboard Initial State](https://i.imgur.com/example1.png)
*Clean interface with sport selection, player input fields, and analysis options ready for data entry.*

#### **Dashboard with Data Entry**
![Dashboard with Data](https://i.imgur.com/example2.png)
*Example analysis for LeBron James showing player information, statistics selection, and ready-to-generate state.*

#### **Complete Analysis Dashboard**
![Complete Analysis](https://i.imgur.com/example3.png)
*Full dashboard showing LeBron James' PTS performance with color-coded bars, team defense rankings, probability distribution, and betting recommendations.*

## 📈 **Supported Statistics & Metrics**

### **NBA Analytics**
- **Basic Metrics**: PTS, REB, AST, STL, BLK, 3PM, FTM, TOV
- **Advanced Combinations**: PRA (PTS+REB+AST), PR (PTS+REB), PA (PTS+AST), RA (REB+AST)
- **Efficiency Metrics**: True Shooting %, Plus/Minus

### **NFL Analytics**
- **Passing Metrics**: PASS_YDS, TD, INT, SACK
- **Rushing Metrics**: RUSH_YDS, Rushing TD
- **Receiving Metrics**: REC_YDS, Receiving TD
- **Combined Metrics**: PRA (PASS_YDS+RUSH_YDS+REC_YDS)

### **NHL Analytics**
- **Scoring Metrics**: GOALS, ASSISTS, POINTS
- **Physical Metrics**: HITS, BLOCKS, Penalty Minutes
- **Advanced Metrics**: Plus/Minus

### **WNBA Analytics**
- **Complete Coverage**: All NBA metrics adapted for women's basketball
- **Advanced Metrics**: Same statistical rigor as NBA analysis

## 🛠️ **Technology Stack**

### **Core Technologies**
- **Python 3.8+**: Modern Python with type hints
- **Tkinter**: Cross-platform GUI framework
- **Matplotlib**: Professional data visualization
- **BeautifulSoup**: Web scraping capabilities
- **NumPy/Pandas**: High-performance data processing
- **Requests**: HTTP client for API integration

### **Quality Features**
- **Error Handling**: Robust exception handling with graceful fallbacks
- **Testing**: Unit tests and integration testing
- **Code Quality**: PEP 8 compliance with documentation
- **Performance**: Optimized algorithms for real-time analysis

## 📋 **Usage Examples**

### **Basic Analysis**
```python
# Launch dashboard
python quick_start.py

# Select NBA, enter "Stephen Curry", choose PTS, set projection to 30.5
# View comprehensive analysis with hit probability and recommendations
```

### **Advanced Analytics**
```python
# Use WMA (Weighted Moving Average) for trend analysis
# Select combined statistics like PRA for comprehensive player evaluation
# Analyze team defense matchups for strategic decisions
```

## 🤝 **Contributing**

### **Development Workflow**
1. Fork the repository
2. Create feature branch (`git checkout -b feature/new-analytics`)
3. Implement changes with testing
4. Commit with descriptive messages (`git commit -m 'Add new statistical analysis'`)
5. Push to branch (`git push origin feature/new-analytics`)
6. Open Pull Request with description

### **Code Standards**
- **PEP 8 Compliance**: Follow Python style guidelines
- **Type Hints**: Use type annotations where helpful
- **Documentation**: Clear comments and docstrings
- **Testing**: Include tests for new features

## 📄 **License & Legal**

This project is licensed under the MIT License - see the LICENSE file for details.

**Important Disclaimer**: This tool is for educational and analysis purposes only. Please gamble responsibly and within your means. The authors are not responsible for any financial losses incurred through the use of this software.

## 🙏 **Acknowledgments**

- **StatMuse**: Primary data source for sports statistics
- **Matplotlib**: Data visualization library
- **BeautifulSoup**: Web scraping framework
- **NumPy/Pandas**: Data processing libraries

## 📞 **Support & Contact**

For questions, issues, or feature requests:
- **GitHub Issues**: Open issues with reproduction steps
- **Documentation**: Check `/docs` directory for guides
- **Examples**: Working examples in `/examples` directory
- **Testing**: Run `python -m pytest tests/` for testing

---

**Built for sports analytics enthusiasts**

*This platform combines real-time data processing, statistical modeling, and intuitive interfaces to provide insights for sports betting decisions.*

