from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Initialize the ChromeDriver using WebDriverManager
from selenium.webdriver.chrome.service import Service

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Replace with the URL of the webpage you want to scrape
# url = "https://www.friends2support.org/"
url = "https://www.friends2support.org/inner/news/searchresult.aspx"
driver.get(url)

# Wait for the page to load and first dropdown to be present
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "dpBloodGroup")))

# Predefined lists for dropdown values
blood_groups = ['A+', 'A-', 'A1+', 'A1-', 'A1B+', 'A1B-', 'A2+', 'A2-', 'A2B+', 'A2B-', 'AB+', 'AB-', 'B+', 'B-', 'Bombay Blood Group', 'INRA', 'O+', 'O-']  # Extend this list as needed
countries = ['INDIA', 'YEMEN-اليمن', 'NEPAL', 'SRI LANKA', 'BANGLADESH', 'MALAYSIA', 'OMAN']  # You can add more countries if needed
states = ['Andaman and Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh', 'Dadra and Nagar Haveli', 'Daman and Diu', 'Delhi', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu and Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Lakshadweep', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Pondicherry', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal']  # Extend with states for the selected country
districts = {
    'Andaman and Nicobar Islands': ['Andaman And Nicobar', 'Port Blair'], 
    'Andhra Pradesh': ['Anantapur', 'Chittor', 'East Godavari', 'Guntur', 'Kadapa', 'Krishna', 'Kurnool', 'Nellore', 'Prakasam', 'Srikakulam', 'Vishakapatnam', 'Vizianagaram', 'West Godavari'], 
    "Tamil Nadu": ["Kanyakumari", "Chennai"], 
    "Karnataka": ["Bangalore Urban", "Mysore"]
}
cities = {
    'Andaman And Nicobar': ['Bombooflat', 'Car Nicobar', 'Garacharma'], 
    'Port Blair': ['Port Blair'], 
    
    "Kanyakumari": ["Nagercoil", "Thuckalay"], 
    "Chennai": ["Chennai"], 
    "Bangalore Urban": ["Bangalore"], 
    "Mysore": ["Mysore"]
}

# Function to handle the dropdown selection and scraping
def select_and_scrape(blood_group, country, state, district, city):
    # Select Blood Group
    dropdown1 = Select(driver.find_element(By.ID, "dpBloodGroup"))
    dropdown1.select_by_visible_text(blood_group)
    time.sleep(3)  # Give time to load data

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "dpCountry")))
    dropdown2 = Select(driver.find_element(By.ID, "dpCountry"))
    dropdown2.select_by_visible_text(country)
    time.sleep(3)  # Give time to load data
    
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "dpState")))
    dropdown3 = Select(driver.find_element(By.ID, "dpState"))
    dropdown3.select_by_visible_text(state)
    time.sleep(3)  # Give time to load data
    
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "dpDistrict")))
    dropdown4 = Select(driver.find_element(By.ID, "dpDistrict"))
    dropdown4.select_by_visible_text(district)
    time.sleep(3)  # Give time to load data
    
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "dpCity")))
    dropdown5 = Select(driver.find_element(By.ID, "dpCity"))
    dropdown5.select_by_visible_text(city)
    time.sleep(3)  # Give time to load data
    
    # Click the search button
    search_button = driver.find_element(By.ID, "btnSearchDonor")
    search_button.click()
    time.sleep(3)  # Wait for search results to load

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//table[@id="dgBloodDonorResults"]')))
    
    # Determine the number of pages
    pagination = driver.find_element(By.XPATH, "//td[@colspan='4']")
    page_links = pagination.find_elements(By.TAG_NAME, "a")
    total_pages = len(page_links) + 1  # Including the current page

    # Scrape the table data from all pages
    for page in range(total_pages):
        # Scrape the table on the current page
        table = driver.find_element(By.ID, 'dgBloodDonorResults')

        # Extract table rows
        rows = table.find_elements(By.TAG_NAME, "tr")

        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) >= 3:
                name = cols[0].text
                mobile_no = cols[2].text  # Get the mobile number from the 3rd column
                # Create the SQL query for each row
                sql_query = f"INSERT INTO bloogdonnerslist (dpBloodGroup, dpCountry, dpState, dpDistrict, dpCity, Name, `Mobile No.`) VALUES ('{blood_group}', '{country}', '{state}', '{district}', '{city}', '{name}', '{mobile_no}');"
                all_sql_queries.append(sql_query)

        # If there are more pages, click the next page link
        if page < total_pages - 1:
            next_link = page_links[page]  # Get the link for the next page
            next_link.click()  # Click the next page link
            time.sleep(3)  # Wait for the next page to load

# Store all SQL queries
all_sql_queries = []

# Iterate through all dropdown combinations and scrape the data
for blood_group in blood_groups:
    for country in countries:
        for state in states:
            for district in districts[state]:
                for city in cities[district]:
                    select_and_scrape(blood_group, country, state, district, city)

# Save the SQL queries to a file
with open('insert_queries.sql', 'w') as file:
    for query in all_sql_queries:
        file.write(query + "\n")

# Close the browser session
driver.quit()

print("SQL queries have been generated and saved as 'insert_queries.sql'.")