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
url = "https://www.friends2support.org/"
driver.get(url)

# Wait for the page to load and first dropdown to be present
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "dpBloodGroup")))

# Function to select a dropdown option with error handling
def select_dropdown_option(element_id, option_text):
    try:
        dropdown = Select(driver.find_element(By.ID, element_id))
        dropdown.select_by_visible_text(option_text.strip())  # Strip any extra spaces
        print(f"Selected {option_text} in {element_id}")
        return True
    except Exception as e:
        print(f"Could not locate element with visible text: {option_text} in {element_id}. Error: {e}")
        return False

# List to store SQL queries
all_sql_queries = []

# Predefined blood groups and country
blood_groups = [
    "A+", "A-", "A1+", "A1-", "A1B+", "A1B-", 
    "A2+", "A2-", "A2B+", "A2B-", "AB+", "AB-", 
    "B+", "B-", "O+", "O-"
]

countries = ["INDIA"]

# Iterate over the predefined blood groups
for blood_group in blood_groups:
    select_dropdown_option("dpBloodGroup", blood_group)
    time.sleep(3)

    # Iterate over the predefined countries (only INDIA)
    for country in countries:
        select_dropdown_option("dpCountry", country)
        time.sleep(3)

        # Extract states based on the selected country
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "dpState")))
        dropdown3 = Select(driver.find_element(By.ID, "dpState"))
        states = [option.text for option in dropdown3.options if option.text not in ['-----Select-----', 'ALL']]

        for state in states:
            select_dropdown_option("dpState", state)
            time.sleep(3)

            # Extract districts based on the selected state
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "dpDistrict")))
            dropdown4 = Select(driver.find_element(By.ID, "dpDistrict"))
            districts = [option.text for option in dropdown4.options if option.text not in ['-----Select-----', 'ALL']]

            for district in districts:
                select_dropdown_option("dpDistrict", district)
                time.sleep(3)

                # Extract cities based on the selected district
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "dpCity")))
                dropdown5 = Select(driver.find_element(By.ID, "dpCity"))
                cities = [option.text for option in dropdown5.options if option.text not in ['-----Select-----', 'ALL']]

                for city in cities:
                    if not select_dropdown_option("dpCity", city):
                        continue  # Skip this city if not found
                    time.sleep(3)

                    # Click the search button and wait for results
                    search_button = driver.find_element(By.ID, "btnSearchDonor")
                    search_button.click()

                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//table[@id="dgBloodDonorResults"]')))

                    # Determine the number of pages
                    try:
                        pagination = driver.find_element(By.XPATH, "//td[@colspan='4']")
                        page_links = pagination.find_elements(By.TAG_NAME, "a")
                        total_pages = len(page_links) + 1  # Including the current page
                    except Exception:
                        total_pages = 1  # If there's no pagination, it's a single page

                    # Scrape the table data from all pages
                    for page in range(total_pages):
                        table = driver.find_element(By.ID, 'dgBloodDonorResults')

                        # Extract table rows
                        rows = table.find_elements(By.TAG_NAME, "tr")

                        for row in rows[1:]:  # Skip the header row
                            cols = row.find_elements(By.TAG_NAME, "td")
                            if len(cols) >= 3:
                                name = cols[0].text
                                mobile_no = cols[2].text  # Corrected to get the mobile number from the 3rd column
                                # Create the SQL query for each row
                                sql_query = f"INSERT INTO bloogdonnerslist (dpBloodGroup, dpCountry, dpState, dpDistrict, dpCity, Name, `Mobile No.`) VALUES ('{blood_group}', '{country}', '{state}', '{district}', '{city}', '{name}', '{mobile_no}');"
                                all_sql_queries.append(sql_query)

                        # If there are more pages, click the next page link
                        if page < total_pages - 1:
                            pagination = driver.find_element(By.XPATH, "//td[@colspan='4']")  # Re-locate pagination
                            page_links = pagination.find_elements(By.TAG_NAME, "a")  # Re-locate page links
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