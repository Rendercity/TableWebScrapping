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
blood_group = "A+"  # Example value
dropdown1.select_by_visible_text(blood_group)

time.sleep(3)

dropdown2 = Select(driver.find_element(By.ID, "dpCountry"))
country = "INDIA"  # Example value
dropdown2.select_by_visible_text(country)

time.sleep(3)

WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "dpState")))
dropdown3 = Select(driver.find_element(By.ID, "dpState"))
state = "Tamil Nadu"  # Example value
dropdown3.select_by_visible_text(state)

time.sleep(3)

WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "dpDistrict")))
dropdown4 = Select(driver.find_element(By.ID, "dpDistrict"))
district = "Kanyakumari"  # Example value
dropdown4.select_by_visible_text(district)

time.sleep(3)

WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "dpCity")))
dropdown5 = Select(driver.find_element(By.ID, "dpCity"))
city = "Nagercoil"  # Example value
dropdown5.select_by_visible_text(city)

time.sleep(3)

search_button = driver.find_element(By.ID, "btnSearchDonor")
search_button.click()

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//table[@id="dgBloodDonorResults"]')))

# Determine the number of pages
pagination = driver.find_element(By.XPATH, "//td[@colspan='4']")
page_links = pagination.find_elements(By.TAG_NAME, "a")
total_pages = len(page_links) + 1  # Including the current page

# Scrape the table data from all pages
all_sql_queries = []

for page in range(total_pages):
    # Scrape the table on the current page
    table = driver.find_element(By.ID, 'dgBloodDonorResults')

    # Extract table rows
    rows = table.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) >= 3:
            name = cols[0].text
            mobile_no = cols[2].text  # Corrected to get the mobile number from the 3rd column
            # Create the SQL query for each row
            sql_query = f"INSERT INTO bloogdonnerslist (dpBloodGroup, dpCountry, dpState, dpDistrict, dpCity, Name, `Mobile No.`) VALUES ('{blood_group}', '{country}', '{state}', '{district}', '{city}', '{name}', '{mobile_no}');"
            all_sql_queries.append(sql_query)

    # If there are more pages, click the next page link
    if page < total_pages - 1:
        next_link = page_links[page]  # Get the link for the next page
        next_link.click()  # Click the next page link
        time.sleep(3)  # Wait for the next page to load

# Save the SQL queries to a file
with open('insert_queries.sql', 'w') as file:
    for query in all_sql_queries:
        file.write(query + "\n")

# Close the browser session
driver.quit()

print("SQL queries have been generated and saved as 'insert_queries.sql'.")
