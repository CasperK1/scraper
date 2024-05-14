import requests
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

url = "https://web-api.service.verkkokauppa.com/search?filter=category%3Agraphics_processors&private=true&sessionId=b5150716-01f9-4165-851f-46539ab92567&pageNo=0&pageSize=48&sort=price%3Aasc&lang=fi&query=rtx+4090"


def get_data_verkkokauppa():
    try:
        response = requests.request("GET", url)
        data = response.json()
        product_count = 1

        if 'products' not in data:
            print("ERROR: No products found in the response.")
            return

        for product in data['products']:
            if (product["availability"]["overrideText"] != "ei tiedossa"
                    and product["availability"]["overrideText"] != "Ei vahvistettu"
                    and product["availability"]["isPurchasable"] == True):
                print(f"#{product_count} {product['name']} {product['price']["currentFormatted"]}e\n")
                product_count += 1
        logging.info("FETCHED FROM VERKKOKAUPPA")

    except Exception as e:
        logging.info(f"ERROR: An unexpected error occurred. Details: {str(e)}")
        return


