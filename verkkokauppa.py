import httpx
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



def get_product_details(product):
    if (product["availability"]["overrideText"] != "ei tiedossa"
            and product["availability"]["overrideText"] != "Ei vahvistettu"
            and product["availability"]["isPurchasable"] == True):
        gpu = {
            'name': product['name'],
            'price': product['price']['currentFormatted'],
        }
        return gpu


async def get_data_verkkokauppa():
    url = "https://web-api.service.verkkokauppa.com/search?filter=category%3Agraphics_processors&private=true&sessionId=b5150716-01f9-4165-851f-46539ab92567&pageNo=0&pageSize=48&sort=price%3Aasc&lang=fi&query=rtx+4090"
    product_count = 1
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            data = response.json()

            if 'products' not in data:
                logging.error("No products found in the response.")
                return

            for product in data['products']:
                gpu = get_product_details(product)
                if gpu:
                    print(f"VERKKIS #{product_count} {gpu['name']} {gpu['price']}e\n")
                    product_count += 1

        logging.info("FETCHED FROM VERKKOKAUPPA")

    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error occurred: {str(e)}")
    except httpx.RequestError as e:
        logging.error(f"Request error occurred: {str(e)}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")

