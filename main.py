import logging
import asyncio
from utils.timer import timer
from scrapers import get_data_verkkokauppa, get_data_datatronic, get_data_jimms, get_data_proshop, get_data_wolt
from db.db_connect import Database
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# TODO : compare identical product prices (EAN code?), Frontend....


@timer
async def main():
    options = Options()  # Selenium boilerplate
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    x = input("Input 1: rtx 4090 prices\nInput 2: Wolt discounts\nInput 3: Both\nInput 4: exit\n >> ")
    if x == "1" or x == "3":
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

    if x == "2" or x == "3":
        get_data_wolt(driver, "Patruunakatu 8")

    if x == "4":
        print("Exiting...")
        return


if __name__ == "__main__":
    asyncio.run(main())
