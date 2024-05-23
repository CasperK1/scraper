import logging
import asyncio
from utils.timer import timer
from scrapers import get_data_verkkokauppa, get_data_datatronic, get_data_jimms
from db.db_connect import database
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# TODO 1: implement aiosqlite
# TODO 2: compare identical product prices (EAN code?), Frontend....



@timer
async def main():
    #options = Options()  # Selenium boilerplate
    #options.add_argument("--headless=new")
    #driver = webdriver.Chrome(options=options)
    with database("prices.db") as db:
        try:
            # Run all tasks concurrently
            await asyncio.gather(
                get_data_verkkokauppa(db),
                get_data_datatronic(db),
                get_data_jimms(db)

            )

        except Exception as e:
            logging.error(f"An unexpected error occurred in main.py: {str(e)}")




if __name__ == "__main__":
    asyncio.run(main())
