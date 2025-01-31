from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
import pandas as pd
import time

# URL of the website to scrape
url = 'https://www.imdb.com/title/tt0097165/reviews/'

# Open selenium webdriver
driver = webdriver.Chrome()

# Load the page
try:
    driver.get(url)
except Exception as e:
    print(e)
    driver.quit()
    
expand_button = driver.find_elements(By.CSS_SELECTOR, 'button.ipc-see-more__button')[1]

driver.execute_script("arguments[0].scrollIntoView();", expand_button)
time.sleep(2)
expand_button.click()

import time

last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Wait for new content to load
    new_height = driver.execute_script("return document.body.scrollHeight")
    
    if new_height == last_height:
        break  # Stop if no new content is loaded
    last_height = new_height


WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'div.ipc-list-card__content'))
)

# Now scrape the elements
elements = driver.find_elements(By.CSS_SELECTOR, 'div.ipc-list-card__content')

review_df = pd.DataFrame(columns=['Title', 'Review', 'Rating'])

for element in elements:
    try:
        rating = element.find_element(By.CSS_SELECTOR, 'span.ipc-rating-star--rating').text
        title = element.find_element(By.CSS_SELECTOR, 'h3.ipc-title__text').text
        review = element.find_element(By.CSS_SELECTOR, 'div.ipc-html-content-inner-div').text
        new_row = pd.DataFrame([{'Title': title, 'Review': review, 'Rating': rating}])
        review_df = pd.concat([review_df, new_row], ignore_index=True)
    except Exception as e:
        print(e)
        continue
# Save the dataframe to a csv file
review_df.to_csv('reviews.csv', index=False)