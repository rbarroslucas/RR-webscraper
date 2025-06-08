from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def get_all_product_links(driver, url, base_url):
    driver.get(url)
    all_products = []

    while True:
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#rankings-list li.product_list"))
            )
            time.sleep(1)

            product_items = driver.find_elements(By.CSS_SELECTOR, "#rankings-list li.product_list")

            for item in product_items:
                try:
                    name_elem = item.find_element(By.CSS_SELECTOR, ".product-name a span")
                    name = name_elem.text.strip()

                    link_elem = item.find_element(By.CSS_SELECTOR, ".product-name a")
                    relative_link = link_elem.get_attribute("href")
                    link = relative_link if relative_link.startswith("http") else base_url + relative_link


                    all_products.append((name, link))
                except Exception as e:
                    print(e)
                    continue

            next_buttons = driver.find_elements(By.CSS_SELECTOR, ".paginate-buttons.next-button")
            if not next_buttons:
                break  

            next_button = next_buttons[0]
            if "disabled" in next_button.get_attribute("class"):
                break

            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_button)
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".paginate-buttons.next-button"))
            )
            next_button.click()
            time.sleep(2)

        except Exception as e:
            print(e)
            break

    return all_products
