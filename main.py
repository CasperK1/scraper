import logging
import asyncio
from utils.timer import timer
from scrapers import get_data_verkkokauppa, get_data_datatronic, get_data_jimms
from db.db_connect import database
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# TODO: implement aiosqlite, dont insert duplicates, compare identical product prices (EAN code?)
# TODO: Frontend....



@timer
async def main():
    options = Options()  # Selenium boilerplate
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    with database("prices.db") as db:
        try:
            # Run all tasks concurrently
            await asyncio.gather(
                asyncio.to_thread(get_data_jimms, driver, db),  # to_thread = Selenium does not support async
                get_data_verkkokauppa(db),
                get_data_datatronic(db)
            )

        except Exception as e:
            logging.error(f"An unexpected error occurred: {str(e)}")

        finally:
            driver.quit()


if __name__ == "__main__":
    asyncio.run(main())
