import time
import logging
import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
from bs4 import BeautifulSoup


def get_product_details(product_card):
    product_title = product_card.find("h3", class_="h3 product-title").text.strip()
    product_price = product_card.find("span", class_="price").text.strip()
    if product_title and "4090" in product_title:
        gpu = {
            'name': product_title,
            'price': product_price,
        }
        return gpu
    else:
        return


def get_data_datatronic():
    page_nmbr = 1
    product_nmbr = 1
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    while True:
        try:
            response = requests.get(f"https://datatronic.fi/haku?s=rtx+4090&ajs_cat=15&fast_search=fs&order=product.price.asc&page={str(page_nmbr)}", headers)
            html = response.text
            soup = BeautifulSoup(html, "lxml")
            gpus = soup.find_all("article", class_="product-miniature js-product-miniature")
            page_not_found = soup.find("section", class_="page-content page-not-found")
            if not page_not_found and gpus:
                for gpu_product_card in gpus:
                    gpu = get_product_details(gpu_product_card)
                    if gpu:
                        print(f"#{product_nmbr} Product Name: {gpu['name']}\nPrice: {gpu['price']}\n")
                        product_nmbr+=1
                page_nmbr += 1
            else:
                logging.info(f'FETCHED FROM DATATRONIC. NUMBER OF PAGES REQUESTED: {page_nmbr - 1}')
                break

        except requests.exceptions.RequestException as e:
            print(f"ERROR: {str(e)}")


