import logging
import asyncio
from utils.timer import timer
from scrapers import get_data_verkkokauppa, get_data_datatronic, get_data_jimms, get_data_proshop
from db.db_connect import Database
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# TODO : compare identical product prices (EAN code?), Frontend....


@timer
async def main():
    # options = Options()  # Selenium boilerplate
    # options.add_argument("--headless=new")
    # driver = webdriver.Chrome(options=options)
    #x = input("Input 1: rtx 4090 prices\nInput 2: Wolt discounts\n")

    with Database("prices.db") as db:
        try:
            # Run all tasks concurrently
            await asyncio.gather(
                get_data_verkkokauppa(db),
                get_data_datatronic(db),
                get_data_jimms(db),
                get_data_proshop(db)

            )

        except Exception as e:
            logging.error(f"An unexpected error occurred in main.py: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())
