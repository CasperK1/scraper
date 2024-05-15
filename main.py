import logging
import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from timer import timer

from jimms import get_data_jimms
from verkkokauppa import get_data_verkkokauppa
from datatronic import get_data_datatronic


# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@timer
async def main():
    options = Options()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    try:
        # Run all tasks concurrently
        await asyncio.gather(
            asyncio.to_thread(get_data_jimms, driver), # Selenium does not support async
            get_data_verkkokauppa(),
            get_data_datatronic()
        )

    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")

    finally:
        driver.quit()


if __name__ == "__main__":
    asyncio.run(main())
