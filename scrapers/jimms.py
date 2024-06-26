import httpx
import logging


def get_product_details(product):
    if product['ProductGroupID'] == "000-213" and "4090" in product['Name']:
        return {'name': product['Name'], 'price': product['PriceTax']}


async def get_data_jimms(db):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    product_nmbr = 0
    try:
        async with httpx.AsyncClient(headers=headers) as client:
            response = await client.post(
                'https://www.jimms.fi/api/product/newbetasearch?1716452629617',
                json={"SearchQuery": "rtx 4090"}
            )
            response.raise_for_status()
            data = response.json()

            if 'Products' not in data:
                logging.error("No products found in the response.")
                return

            for product in data['Products']:
                gpu = get_product_details(product)
                if gpu:
                    db.insert("jimms", gpu['name'], gpu['price'])
                    #print(f"JIMMS #{product_nmbr} {gpu['name']} {gpu['price']}e\n")
                    product_nmbr += 1

        logging.info(f"FETCHED FROM JIMMS. NUMBER OF PRODUCTS: {product_nmbr}\n")


    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error occurred: {str(e)}")
    except httpx.RequestError as e:
        logging.error(f"Request error occurred: {str(e)}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")


