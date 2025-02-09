import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


def get_product_details(product_card, title_tag, title_class, product_tag, product_class):
    product_title = product_card.find(title_tag, class_=title_class).text.strip()
    product_price = product_card.find(product_tag, class_=product_class).text.strip()
    price_formatted = product_price.replace('\xa0', '').replace('€', '').replace(',', '.')
    if product_title and "4090" in product_title:
        return {'name': product_title, 'price': float(price_formatted)}


def get_data_jimms(driver, db):
    try:
        driver.get("https://www.jimms.fi/fi/Product/Search?i=100&ob=4&q=rtx%204090&fg=000-1N0")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'product-box'))
        )
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        product_div = soup.find_all('product-box')

        if product_div:
            product_nmbr = 0
            for gpu_product_card in product_div:
                gpu = get_product_details(gpu_product_card, 'a', 'text-reset text-decoration-none js-gtm-product-link',
                                          "span", "price__amount")
                if gpu:
                    db.insert("jimms", gpu['name'], gpu['price'])
                    product_nmbr += 1
        else:
            logging.error('FINISHED. NOTHING FOUND.')
            return

        logging.info(f"FETCHED FROM JIMMS. NUMBER OF PRODUCTS: {product_nmbr}\n")

    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")