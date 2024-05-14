import logging
from jimms import get_data_jimms
from verkkokauppa import get_data_verkkokauppa
from datatronic import get_data_datatronic
from selenium import webdriver
from timer import timer

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


@timer
def main():
    driver = webdriver.Chrome()
    try:
        logging.info("Starting to fetch data from Jimms...")
        get_data_jimms(driver)
        if driver:
            driver.quit()
            logging.info("Web driver has been closed.")

        logging.info("Starting to fetch data from Verkkokauppa...")
        get_data_verkkokauppa()

        logging.info("Starting to fetch data from Datatronic...")
        get_data_datatronic()

    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")


if __name__ == "__main__":
    main()
