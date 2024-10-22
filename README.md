# Stock Investment Recommendation Scraper

## Overview
The **Stock Investment Recommendation Scraper** is a Python-based tool that scrapes stock recommendations from multiple financial platforms. It gathers stock data from platforms like **HDFC Securities**, **ICICI Securities**, **5Paisa**, and **Moneycontrol**, sorting them based on the potential upside of the stocks, allowing users to easily find top investment options.

### Features
- Scrapes stock data from 4 major platforms: 
  - HDFC Securities
  - ICICI Securities
  - 5Paisa
  - Moneycontrol
- Automatically sorts the stocks by potential upside in descending order.
- Handles web-based popups and overlays using Selenium to ensure smooth scraping.
- Outputs the top 10 stock recommendations from each site.

## Requirements
Ensure the following Python packages are installed:

```plaintext
selenium
requests
```
## How to Use

### 1. Clone the repository

You can clone this repository using Git:

```bash
git clone https://github.com/YourUsername/YourRepositoryName.git
```

### 2. Navigate to the project directory

Use `cd` to navigate into the cloned project directory:

```bash
cd Stock-Investment-Recommendation-Scraper

```

### 3. Install dependencies
Make sure you have Python installed. Then, use pip to install the dependencies from requirements.txt
```bash
pip install -r requirements.txt
```
### 4. Run the project
To run the scraping program, use the following command:
```bash
python Main.py
```
### Note:
Ensure you have ChromeDriver installed and set the correct path to your ChromeDriver executable in the script:
```bash
driver_path = r"Path\to\your\chromedriver.exe"
```


### 5. Customize the script (Optional)

If you want to add more stock sources or customize the scraping functionality, you can modify the scraping functions in `Main.py`. Each function corresponds to a different website:

- `scrape_hdfcsec()`: Scrapes stock recommendations from HDFC Securities.
- `scrape_icici()`: Scrapes stock recommendations from ICICI Direct.
- `scrape_5paisa()`: Scrapes stock recommendations from 5Paisa.
- `scrape_moneycontrol()`: Scrapes stock recommendations from the Moneycontrol API.

Feel free to expand the scraper by adding new platforms.

### 6. Future Enhancements

- **Add more stock platforms**: Expand the scraper to other stock recommendation websites.
- **Add data export**: Export the stock recommendation data to CSV or other formats.
- **Improve API support**: Direct integration with more APIs for better data accuracy and speed.
