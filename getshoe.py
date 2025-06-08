from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def find(selector, driver, by=By.CSS_SELECTOR, get_attr=None, index=0):
    try:
        elements = driver.find_elements(by, selector)
        if not elements:
            return ""
        element = elements[index]
        return element.get_attribute(get_attr) if get_attr else element.text.strip()
    except:
        return ""

def get_review_date(driver):
    try:
        div = driver.find_element(By.CSS_SELECTOR, ".author-name")
        parts = div.text.strip().split("on ")
        if len(parts) == 2:
            return parts[1].strip()
        return ""
    except:
        return ""

def get_ratings(driver):
    try:
        score_element = driver.find_element(By.CSS_SELECTOR, "[class*='trigger-popover-']")

        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", score_element)
        ActionChains(driver).move_to_element(score_element).perform()

        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.popover .corescore-explainer-scores"))
        )

        popover = driver.find_element(By.CSS_SELECTOR, "div.popover .corescore-explainer-scores")
        source_ratings = popover.find_elements(By.CSS_SELECTOR, "div")
        ratings = [el.text.strip() for el in source_ratings if el.text.strip()]
        return " | ".join(ratings)

    except Exception as e:
        return ""


def extract_comparison_details(driver):
    comparison_data = {}
    rows = driver.find_elements(By.CSS_SELECTOR, ".simple-comparison tbody tr")
    for row in rows:
        try:
            label = row.find_element(By.CSS_SELECTOR, "th .fact-label").text.strip()
            cell = row.find_element(By.CSS_SELECTOR, "td.similar-comparison-data-first")
            values = cell.find_elements(By.CLASS_NAME, "fact-value")
            if values:
                comparison_data[label] = ", ".join([val.text.strip() for val in values])
            else:
                try:
                    parent = cell.find_element(By.CLASS_NAME, "similar-comparison-data-body")
                    full_text = parent.text.strip()
                    spans = parent.find_elements(By.TAG_NAME, "span")
                    span_texts = [s.text.strip() for s in spans if s.text.strip()]
                    if span_texts and full_text.startswith("#"):
                        main_value = full_text.replace(span_texts[0], "").strip()
                        comparison_data[label] = main_value
                        comparison_data[label + "Percentile"] = span_texts[0]
                    else:
                        comparison_data[label] = full_text
                except:
                    comparison_data[label] = cell.text.strip()
        except:
            continue
    return comparison_data


def scrape_product_data(url, driver):
    driver.get(url)

    shoe = {
        "url": url,
        "shoe_name": find("li.breadcrumb-item.active span", driver) or find("#product-title .main-shoe-title", driver),
        "brand": find("brand-value", driver, By.CLASS_NAME),
        "total_score": find("corescore-big__score", driver, By.CLASS_NAME),
        "pros": "; ".join([el.text for el in driver.find_elements(By.CSS_SELECTOR, "#the_good li")]),
        "cons": "; ".join([el.text for el in driver.find_elements(By.CSS_SELECTOR, "#the_bad li")]),
        "RR_verdict": find("#product-intro .product-intro-verdict + div", driver),
        "awards": ", ".join([item.text.strip() for item in driver.find_elements(By.CSS_SELECTOR, ".awards-list__item") if item.text.strip()]),
        "external_ratings": get_ratings(driver),
        "review_date": get_review_date(driver),
        "terrain": find("terrain-value", driver, By.CLASS_NAME),
        "arch": find("arch-support-value", driver, By.CLASS_NAME),
        "use": ", ".join([el.text.strip() for el in driver.find_elements(By.CSS_SELECTOR, ".use-value > *") if el.text.strip() and el.text.strip() != "|"]),
        "shoe_weight": find("weight-value", driver, By.CLASS_NAME),
        "toe_drop": find("heel-to-toe-drop-value", driver, By.CLASS_NAME),
        "foot_height": find("forefoot-height-value", driver, By.CLASS_NAME),
    }
    try:
        see_more_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.btn-expand.btn-default")))
        time.sleep(1)
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", see_more_btn)
        see_more_btn.click()
        time.sleep(1)
    except:
        pass
    shoe.update(extract_comparison_details(driver))
    return shoe
