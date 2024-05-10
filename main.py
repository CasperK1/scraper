from selenium import webdriver
from bs4 import BeautifulSoup
import time



def scrape(driver):
    driver.get('https://www.verkkokauppa.com/fi/search?query=rtx%204090')
    time.sleep(0.4)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    products = soup.find_all('li', class_="sc-1twc5z9-1 iIZx")
    for product in products:
        print(product.a.text)

if __name__ == "__main__":
    driver = webdriver.Chrome()

    scrape(driver)