import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
from bs4 import BeautifulSoup


def get_product_details(product_card, title_tag, title_class, product_tag, product_class):
    product_title = product_card.find(title_tag, class_=title_class).text.strip()
    product_price = product_card.find(product_tag, class_=product_class).text.strip()
    if product_title and "4090" in product_title:
        gpu = {
            'name': product_title,
            'price': product_price,
        }
        return gpu


def get_data_jimms(driver):
    try:
        driver.get("https://www.jimms.fi/fi/Product/Search?i=100&ob=4&q=rtx%204090&fg=000-1N0")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'product-box'))
        )
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        product_div = soup.find_all('product-box')

        if product_div:
            product_nmbr = 1
            for gpu_product_card in product_div:
                gpu = get_product_details(gpu_product_card, 'a', 'text-reset text-decoration-none js-gtm-product-link', "span", "price__amount")
                if gpu:
                    print(f"JIMMS #{product_nmbr} Product Name: {gpu['name']}\nPrice: {gpu['price']}\n")
                    product_nmbr += 1
        else:
            logging.error('FINISHED. NOTHING FOUND.')
            return

        logging.info("FETCHED FROM JIMMS")

    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
