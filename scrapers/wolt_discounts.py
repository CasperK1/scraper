import time
import httpx
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

'sc-c2c560a0-1 ggJcnU'
options = Options()  # Selenium boilerplate
# options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)




def get_data_wolt():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    product_nmbr = 0
    try:
        driver.get("https://wolt.com/en/discovery/restaurants?sorting=rating")
        wait = WebDriverWait(driver, 10)
        wait.until(
            EC.element_to_be_clickable((By.XPATH, '//div[contains(text(), "Accept")]'))).click()  # Accept cookies

        # Scroll to the bottom of the page
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                # Wait for the scroll height to increase
                wait.until(lambda d: d.execute_script("return document.body.scrollHeight") > last_height)
                # Update the last_height to the new scroll height after the page has loaded more content
                new_height = driver.execute_script("return document.body.scrollHeight")
                last_height = new_height

            except Exception as e: # Wait for timeout to brake the loop
                break

            # WebDriverWait(driver, 10).until(
            #    EC.presence_of_element_located((By.CSS_SELECTOR,
            #    'sc-2d3d4a7-47 eQnlgy cb-elevated cb_elevation_elevationXsmall_equ2 sc-76d53bc5-1 icKvTn')))





    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error occurred: {str(e)}")
    except httpx.RequestError as e:
        logging.error(f"Request error occurred: {str(e)}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")


get_data_wolt()
