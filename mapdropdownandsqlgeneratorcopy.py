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

# Wait for the page to load
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "dpBloodGroup")))

# Define the dropdown data for mapping
blood_groups = [
    "A+", "A-", "A1+", "A1-", "A1B+", "A1B-", "A2+", "A2-", "A2B+", "A2B-", "AB+", "AB-", "B+", "B-", "O+", "O-"
]
countries = ["INDIA"]  # Limiting to INDIA

# Limiting to two loops for testing purposes
max_data_loops = 2
data_loops = 0

# Iterate over blood groups and countries
for blood_group in blood_groups:
    if data_loops >= max_data_loops:
        break

    # Select blood group
    dropdown1 = Select(driver.find_element(By.ID, "dpBloodGroup"))
    dropdown1.select_by_visible_text(blood_group)
    time.sleep(3)

    for country in countries:
        if data_loops >= max_data_loops:
            break

        # Select country
        dropdown2 = Select(driver.find_element(By.ID, "dpCountry"))
        dropdown2.select_by_visible_text(country)
        time.sleep(3)

        # Select state, district, and city
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "dpState")))
        state_dropdown = Select(driver.find_element(By.ID, "dpState"))
        states = [option.text for option in state_dropdown.options if option.text != "-----Select-----"]

        for state in states:
            if data_loops >= max_data_loops:
                break

            state_dropdown.select_by_visible_text(state)
            time.sleep(3)

            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "dpDistrict")))
            district_dropdown = Select(driver.find_element(By.ID, "dpDistrict"))
            districts = [option.text for option in district_dropdown.options if option.text != "-----Select-----"]

            for district in districts:
                if data_loops >= max_data_loops:
                    break

                district_dropdown.select_by_visible_text(district)
                time.sleep(3)

                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "dpCity")))
                city_dropdown = Select(driver.find_element(By.ID, "dpCity"))
                cities = [option.text for option in city_dropdown.options if option.text != "ALL"]

                for city in cities:
                    if data_loops >= max_data_loops:
                        break

                    city_dropdown.select_by_visible_text(city)
                    time.sleep(3)

                    # Click the search button
                    search_button = driver.find_element(By.ID, "btnSearchDonor")
                    search_button.click()

                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//table[@id="dgBloodDonorResults"]')))

                    # Determine the number of pages
                    pagination = driver.find_element(By.XPATH, "//td[@colspan='4']")
                    page_links = pagination.find_elements(By.TAG_NAME, "a")
                    total_pages = min(len(page_links) + 1, 2)  # Limiting to 2 pages for testing

                    # Scrape the table data from 2 pages for testing
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
                    with open(f'insert_queries_{blood_group}_{state}_{district}_{city}.sql', 'w') as file:
                        for query in all_sql_queries:
                            file.write(query + "\n")

                    # Increment data loop counter
                    data_loops += 1

# Close the browser session
driver.quit()

print("SQL queries have been generated for 2 data loops and saved.")