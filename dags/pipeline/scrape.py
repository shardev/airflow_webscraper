from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from models import CarListing
import time

def scrape_web_data(url):
    driver = webdriver.Chrome()
    driver.get(url)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "articles")))

    titles_elements = driver.find_elements(By.XPATH, "//h1[@class='main-heading normal-heading']")
    prices_elements = driver.find_elements(By.XPATH, "//span[@class='smaller']")
    links_elements = driver.find_elements(By.XPATH, "//a[@class='rounded-5 wrap relative w-full flex rounded-sm']")

    titles = [title.text for title in titles_elements]
    prices = [price.text for price in prices_elements]
    links = [link.get_attribute('href') for link in links_elements]
    
    listings = []
    for title, price, link in zip(titles, prices, links):
        listing = CarListing(link.split('/')[-1], title, price, link)
        listings.append(listing)
        
    driver.close()
    driver.quit()
    
    # Serialize before sending to X-COM
    return [car.to_dict() for car in listings] 
