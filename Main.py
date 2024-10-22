from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import requests
import os
import time

# Path to your ChromeDriver executable
driver_path = r"C:\Users\Asus\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"


# Function to remove any blocking elements using JavaScript (used for ICICI)
def remove_blocking_elements(driver):
    try:
        # Find and remove the blocking image (e.g., the pop-up or any other overlay)
        driver.execute_script("""
            var blockingImage = document.querySelector(".icd-desktop");
            if (blockingImage) {
                blockingImage.remove();
            }
        """)
        time.sleep(2)  # Allow time for the element to be removed

        # Find and close the pop-up if present (the close button)
        close_button = driver.find_element(By.XPATH, "//button[@class='close']")
        if close_button:
            driver.execute_script("arguments[0].click();", close_button)
        time.sleep(2)  # Allow time for the pop-up to close
    except Exception as e:
        print(f"No pop-up to close or error closing it: {e}")


# Function to click the element using JavaScript to avoid click interception (used for ICICI)
def click_element_with_js(driver, element):
    try:
        driver.execute_script("arguments[0].click();", element)
        time.sleep(2)  # Wait after clicking
    except Exception as e:
        print(f"Error clicking element using JavaScript: {e}")


# Function to scrape HDFC Securities
def scrape_hdfcsec():
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument(f"user-data-dir={os.path.join(os.getcwd(), 'chrome-profile')}")

    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get("https://www.hdfcsec.com/research/stock-market-ideas/trading-ideas")
    time.sleep(5)

    stocks = {}
    stock_sections = driver.find_elements(By.CLASS_NAME, 'researchElement')

    if not stock_sections:
        driver.quit()
        return {}

    for section in stock_sections:
        try:
            stock_name = section.find_element(By.CLASS_NAME, 'comp-name').text.strip()
            potential_upside = section.find_element(By.CLASS_NAME, 'circle-val').text.strip()
            potential_upside = float(potential_upside.replace('%', '').strip())
            stocks[stock_name] = potential_upside
        except Exception:
            pass

    driver.quit()
    return stocks


# Function to scrape ICICI Securities
def scrape_icici():
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument(f"user-data-dir={os.path.join(os.getcwd(), 'chrome-profile')}")

    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get("https://www.icicidirect.com/research/equity/investing-ideas")
    time.sleep(5)

    # Attempt to remove blocking elements
    remove_blocking_elements(driver)

    # Scroll to the table header for sorting and click using JavaScript
    try:
        potential_header = driver.find_element(By.XPATH, "//th[contains(text(), 'Potential %')]")
        driver.execute_script("arguments[0].scrollIntoView(true);", potential_header)
        time.sleep(2)  # Give some time for the page to scroll

        # Click the "Potential %" column header twice using JavaScript
        click_element_with_js(driver, potential_header)  # First click to sort in ascending order
        time.sleep(2)  # Wait for sorting
        click_element_with_js(driver, potential_header)  # Second click to sort in descending order
    except Exception as e:
        print(f"Error clicking the Potential % header: {e}")
        driver.quit()
        return {}

    # Now scrape the stocks in the sorted order
    stocks = {}
    stock_rows = driver.find_elements(By.XPATH, "//table[@id='datatableinvestingideas']//tbody//tr")

    if not stock_rows:
        print("No stock data found.")
        driver.quit()
        return {}

    # Extract stock data from each row
    for index, row in enumerate(stock_rows[:10]):  # Limit to top 10 stocks
        try:
            company_name = row.find_element(By.XPATH, "./td[1]/a").text.strip()
            potential_upside = row.find_element(By.XPATH, "./td[5]").text.strip()

            # Handle empty or invalid potential upside
            if potential_upside == '':
                continue

            # Convert potential upside to a float (if it's a percentage)
            potential_upside = float(potential_upside.replace('%', '').strip())

            # Add the stock name and potential upside to the dictionary
            stocks[company_name] = potential_upside

        except Exception as e:
            print(f"Error extracting stock: {e}")

    # Close the WebDriver
    driver.quit()

    return stocks


# Function to scrape 5Paisa Stocks
def scrape_5paisa():
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument(f"user-data-dir={os.path.join(os.getcwd(), 'chrome-profile')}")

    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get("https://www.5paisa.com/share-market-today/stocks-to-buy-or-sell-today")
    time.sleep(5)

    stocks = {}
    stock_rows = driver.find_elements(By.XPATH, "//table[@id='stock-table']//tbody//tr")

    if not stock_rows:
        driver.quit()
        return {}

    for index, row in enumerate(stock_rows[:10]):
        try:
            stock_name = row.find_element(By.XPATH, "./td[1]").text.strip()
            cmp_price = float(row.find_element(By.XPATH, "./td[3]").text.strip())
            target1 = float(row.find_element(By.XPATH, "./td[6]").text.strip())
            potential_change = round(((target1 - cmp_price) / cmp_price) * 100, 2)
            stocks[stock_name] = potential_change
        except Exception:
            pass

    driver.quit()
    return stocks


# Function to scrape Moneycontrol API
def scrape_moneycontrol():
    url = 'https://api.moneycontrol.com/mcapi/v1/broker-research/get-analysts-choice?start=24&limit=24&sortBy=broker_count&deviceType=W'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://www.moneycontrol.com/',
        'Accept': 'application/json',
        'Connection': 'keep-alive'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json().get("data", [])
    except Exception as e:
        print(f"Error fetching data from Moneycontrol: {e}")
        return {}

    stocks = {}
    for stock in data:
        try:
            stock_name = stock.get("stkname", "N/A")
            potential_upside = stock.get("profitPotential", "N/A")
            if potential_upside != "N/A":
                stocks[stock_name] = float(potential_upside)
        except Exception:
            pass

    return stocks


# Main function to scrape all sites, aggregate the results, and sort them
def main():
    all_stocks = {}

    # Scraping each website
    all_stocks.update(scrape_hdfcsec())
    all_stocks.update(scrape_icici())  # Uses the modified ICICI scraping function
    all_stocks.update(scrape_5paisa())
    all_stocks.update(scrape_moneycontrol())

    if not all_stocks:
        print("No stocks to display.")
        return

    # Sorting the aggregated dictionary by potential upside in descending order
    sorted_stocks = sorted(all_stocks.items(), key=lambda x: x[1], reverse=True)

    # Display the sorted stocks
    print("Stocks sorted by potential upside (in descending order):")
    for stock, upside in sorted_stocks:
        print(f"{stock}: {upside}%")

if __name__ == "__main__":
    main()