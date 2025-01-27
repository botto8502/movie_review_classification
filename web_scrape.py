import selenium.webdriver as webdriver
import pandas as pd

# URL of the website to scrape
url = 'https://www.imdb.com/title/tt0097165/reviews/'

# Open selenium webdriver
driver = webdriver.Chrome()
driver.get(url)

# Find the elements to scrape

print("finished")