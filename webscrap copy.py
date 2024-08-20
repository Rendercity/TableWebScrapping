from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Set up Chrome options if necessary (for specific binary paths or headless mode)
from selenium.webdriver.chrome.service import Service

# Initialize the ChromeDriver using WebDriverManager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Replace with the URL of the webpage you want to scrape
url = "https://www.friends2support.org/"
driver.get(url)

# Wait for the page to load (use WebDriverWait instead of sleep for better practice)
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "dpBloodGroup")))

# Interact with the first dropdown
dropdown1 = Select(driver.find_element(By.ID, "dpBloodGroup"))
dropdown1.select_by_visible_text("A+")  # Replace with the actual option

# Add a delay of 10 seconds
time.sleep(10)

# Interact with the second dropdown
dropdown2 = Select(driver.find_element(By.ID, "dpCountry"))
dropdown2.select_by_visible_text("INDIA")  # Replace with the actual option

# Add a delay of 10 seconds
time.sleep(10)

# Wait until the state dropdown is populated and enabled
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "dpState")))

# Interact with the third dropdown
dropdown3 = Select(driver.find_element(By.ID, "dpState"))
dropdown3.select_by_visible_text("Tamil Nadu")  # Replace with the actual option

# Add a delay of 10 seconds
time.sleep(10)

# Wait until the district dropdown is populated and enabled
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "dpDistrict")))

# Interact with the fourth dropdown
dropdown4 = Select(driver.find_element(By.ID, "dpDistrict"))
dropdown4.select_by_visible_text("Kanyakumari")  # Replace with the actual option

# Add a delay of 10 seconds
time.sleep(10)

# Wait until the city dropdown is populated and enabled
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "dpCity")))

# Interact with the fifth dropdown
dropdown5 = Select(driver.find_element(By.ID, "dpCity"))
dropdown5.select_by_visible_text("Nagercoil")  # Replace with the actual option

# Add a delay of 10 seconds
time.sleep(10)

# Click the search button
search_button = driver.find_element(By.ID, "btnSearchDonor")
search_button.click()

# Wait for the table to load after clicking the search button
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//table')))

# Scrape the table data
table = driver.find_element(By.XPATH, '//table')

# Extract table rows
rows = table.find_elements(By.TAG_NAME, "tr")

# Extract table data
table_data = []
for row in rows:
    cols = row.find_elements(By.TAG_NAME, "td")
    cols = [col.text for col in cols]
    table_data.append(cols)

# Convert the list to a pandas DataFrame
df = pd.DataFrame(table_data)

# Save the DataFrame to a CSV file
df.to_csv('table_data.csv', index=False)

# Close the browser session
driver.quit()

print("Table data has been downloaded and saved as 'table_data.csv'.")
