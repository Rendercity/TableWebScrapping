from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Initialize the ChromeDriver using WebDriverManager
from selenium.webdriver.chrome.service import Service

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Replace with the URL of the webpage you want to scrape
url = "https://www.friends2support.org/"
driver.get(url)

# Wait for the page to load
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "dpBloodGroup")))

# Interact with the dropdowns
dropdown1 = Select(driver.find_element(By.ID, "dpBloodGroup"))
dropdown1.select_by_visible_text("A+")

time.sleep(3)

dropdown2 = Select(driver.find_element(By.ID, "dpCountry"))
dropdown2.select_by_visible_text("INDIA")

time.sleep(3)

WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "dpState")))
dropdown3 = Select(driver.find_element(By.ID, "dpState"))
dropdown3.select_by_visible_text("Tamil Nadu")

time.sleep(3)

WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "dpDistrict")))
dropdown4 = Select(driver.find_element(By.ID, "dpDistrict"))
dropdown4.select_by_visible_text("Kanyakumari")

time.sleep(3)

WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "dpCity")))
dropdown5 = Select(driver.find_element(By.ID, "dpCity"))
dropdown5.select_by_visible_text("Nagercoil")

time.sleep(3)

search_button = driver.find_element(By.ID, "btnSearchDonor")
search_button.click()

# Wait for the specific table with ID 'dgBloodDonorResults' to load
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "dgBloodDonorResults")))

# Determine the number of pages
pagination = driver.find_element(By.XPATH, "//td[@colspan='4']")
page_links = pagination.find_elements(By.TAG_NAME, "a")
total_pages = len(page_links) + 1  # Including the current page

# Scrape the specific table data from all pages
all_table_data = []

for page in range(total_pages):
    # Scrape the specific table on the current page
    table = driver.find_element(By.ID, "dgBloodDonorResults")

    # Extract table rows
    rows = table.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        cols = [col.text for col in cols]
        all_table_data.append(cols)

    # If there are more pages, click the next page link
    if page < total_pages - 1:
        next_link = page_links[page]  # Get the link for the next page
        next_link.click()  # Click the next page link
        time.sleep(3)  # Wait for the next page to load

# Convert the list to a pandas DataFrame
df = pd.DataFrame(all_table_data)

# Save the DataFrame to a CSV file
df.to_csv('table_data.csv', index=False)

# Close the browser session
driver.quit()

print("Specific table data from all pages has been downloaded and saved as 'table_data.csv'.")
