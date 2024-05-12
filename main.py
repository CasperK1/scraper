from selenium import webdriver
from bs4 import BeautifulSoup
import time
#verkkokauppa api
#https://web-api.service.verkkokauppa.com/search?private=true&sessionId=88a4d515-ab3f-4bcb-94cc-b2260886a14e&pageNo=0&pageSize=48&sort=score%3Adesc&lang=fi&query=rtx+4090

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