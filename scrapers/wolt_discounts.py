import time
import httpx
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup




# TODO : Search by dish category, more data and frontend implementation


def get_data_wolt(driver, address):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    try:
        driver.get("https://wolt.com/en/discovery/restaurants?sorting=rating")
        wait = WebDriverWait(driver, 5)
        logging.info("Wolt page loaded. Scrolling to bottom...\n")

        # TODO: Solve this without using time.sleep
        address_input(wait, address)

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

            # Using timeout to brake the loop
            except TimeoutException as e:
                logging.info("Reached the bottom of the page. Getting discounts...\n")
                break

        html = driver.page_source
        soup = BeautifulSoup(html, "lxml")
        restaurants = soup.find_all("div",
                                    class_="sc-2d3d4a7-47 eQnlgy cb-elevated cb_elevation_elevationXsmall_equ2 sc-76d53bc5-1 icKvTn")
        count = 1
        for restaurant_card in restaurants:
            # Check for discount restaurants only
            discount_span = restaurant_card.find("span", class_="sc-c2c560a0-1 ggJcnU")
            rating_elements = restaurant_card.find("div", "sc-2d3d4a7-40 jzfKBS")

            if discount_span and "delivery fees" not in discount_span.text and "New" not in discount_span.text:
                #TODO: GET RATING
                print(f"{count}. {restaurant_card.find("h3", class_="sc-2d3d4a7-23 cSKaBt").text}\n"
                      f"Discount: {restaurant_card.find('span', class_='sc-c2c560a0-1 ggJcnU').text}\n"
                      f"Price range: {restaurant_card.find('span', class_='sc-2d3d4a7-41 jvRYSt').text} ")

                if restaurant_card.find("div", class_="sc-2d3d4a7-46 jBnYMn"):
                    print("Wolt Plus: Yes\n")
                else:
                    print("Wolt Plus: No\n")

                count += 1

        driver.quit()




    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error occurred: {str(e)}")
    except httpx.RequestError as e:
        logging.error(f"Request error occurred: {str(e)}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")


def address_input(wait, address):
    # Accept cookies
    cookie_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[contains(text(), "Accept")]')))
    cookie_button.click()

    # Input address
    address_modal = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "sc-86837fd3-7")))
    address_modal.click()
    address_input = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "cb_Input_InputComponent_i1vu")))
    address_input.send_keys(address)
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "sc-3215ab1f-1.kFgRds"))).click()
    time.sleep(2)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//div[contains(text(), "Continue")]'))).click()


