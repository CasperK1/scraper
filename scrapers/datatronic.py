import httpx
import logging
from bs4 import BeautifulSoup



def get_product_details(product_card):
    product_title = product_card.find("h3", class_="h3 product-title").text.strip()
    title_cleaned = ' '.join(product_title.replace('\n', '').split())
    product_price = product_card.find("span", class_="price").text.strip()
    price_formatted = product_price.replace('\xa0', '').replace('€', '').replace(',', '.')

    if product_title and "4090" in product_title:
        return {'name': title_cleaned, 'price': float(price_formatted)}


async def get_data_datatronic(db):
    page_nmbr = 1
    product_nmbr = 1
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    while True:
        try:
            async with httpx.AsyncClient(headers=headers) as client:
                response = await client.get(
                    f"https://datatronic.fi/haku?s=rtx+4090&ajs_cat=15&fast_search=fs&order=product.price.asc&page={page_nmbr}")
                response.raise_for_status()
                html = response.text
                soup = BeautifulSoup(html, "lxml")
                gpus = soup.find_all("article", class_="product-miniature js-product-miniature")
                page_not_found = soup.find("section", class_="page-content page-not-found")

                if not page_not_found and gpus:
                    for gpu_product_card in gpus:
                        gpu = get_product_details(gpu_product_card)
                        if gpu:
                            #print(f"DATATRONIC #{product_nmbr} Product Name: {gpu['name']}\nPrice: {gpu['price']}\n")
                            db.insert("datatronic", gpu['name'], gpu['price'])
                            product_nmbr += 1
                    page_nmbr += 1
                else:
                    logging.info(f'FETCHED FROM DATATRONIC. NUMBER OF PAGES REQUESTED: {page_nmbr - 1}. '
                                 f'NUMBER OF PRODUCTS: {product_nmbr}\n')
                    return


        except httpx.HTTPStatusError as e:
            logging.error(f"HTTP error occurred: {str(e)}")
            break
        except httpx.RequestError as e:
            logging.error(f"Request error occurred: {str(e)}")
            break
        except Exception as e:
            logging.error(f"An unexpected error occurred: {str(e)}")
            break
