import httpx
import logging
from bs4 import BeautifulSoup


def get_product_details(gpu_product_card):
    product_title = gpu_product_card.find("h2", class_="truncate-overflow").text.strip()
    product_price = gpu_product_card.find("span", class_="site-currency-lg").text.strip()
    price_formatted = product_price.replace('\xa0', '').replace(',', '.').replace('€', '')

    if product_title and "4090" in product_title:
        return {'name': product_title, 'price': float(price_formatted)}


async def get_data_proshop(db):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    product_nmbr = 0
    try:
        async with httpx.AsyncClient(headers=headers) as client:
            response = await client.get("https://www.proshop.fi/?c=naeytoenohjaimet&s=rtx+4090&o=1028")
            response.raise_for_status()
            html = response.text
            soup = BeautifulSoup(html, "lxml")
            gpus = soup.find_all("div", class_="col-xs-8 col-lg-9 site-nopadding")
            page_not_found = soup.find(string="Tuloksia ei löytynyt")
            if not page_not_found and gpus:
                for gpu_product_card in gpus:
                    gpu = get_product_details(gpu_product_card)
                    if gpu:
                        db.insert("proshop", gpu["name"], gpu['price'])
                        product_nmbr += 1

            logging.info(f"FETCHED FROM PROSHOP. NUMBER OF PRODUCTS: {product_nmbr}\n")


    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error occurred: {str(e)}")
    except httpx.RequestError as e:
        logging.error(f"Request error occurred: {str(e)}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
