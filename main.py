import os
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from getlinks import get_all_product_links
from getshoe import scrape_product_data

URL = "https://runrepeat.com/catalog/mens-running-shoes"
BASE_URL = "https://runrepeat.com"

if __name__ == "__main__":
    os.makedirs("data/raw", exist_ok=True)

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-infobars")

    driver = webdriver.Chrome(options=options)

    try:
        all_links = get_all_product_links(driver, URL, BASE_URL)   
        with open("data/all_links.json", "w", encoding="utf-8") as f:
            json.dump(all_links, f, ensure_ascii=False, indent=2)

        for name, url in all_links:
            print(f"Scraping: {name}")
            try:
                shoe_data = scrape_product_data(url, driver)
                if shoe_data and shoe_data.get("shoe_name"):
                    filename = name.lower().replace(" ", "_").replace("/", "-")
                    with open(f"data/raw/{filename}.json", "w", encoding="utf-8") as f:
                        json.dump(shoe_data, f, ensure_ascii=False, indent=2)
            except Exception as e:
                print(f"Failed processing {name}: {e}")
    finally:
        driver.quit()
