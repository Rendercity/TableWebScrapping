from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

# Initialize the ChromeDriver using WebDriverManager
from selenium.webdriver.chrome.service import Service

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Replace with the URL of the webpage you want to scrape
url = "https://www.friends2support.org/"
driver.get(url)

# Wait for the page to load and first dropdown to be present
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "dpBloodGroup")))

# Function to extract options from a dropdown
def get_dropdown_options(element_id):
    dropdown = Select(driver.find_element(By.ID, element_id))
    options = [option.text.strip() for option in dropdown.options if option.text != 'Select']
    return options

# Select a dropdown option with error handling
def select_dropdown_option(element_id, option_text):
    try:
        dropdown = Select(driver.find_element(By.ID, element_id))
        dropdown.select_by_visible_text(option_text.strip())  # Strip any extra spaces
        print(f"Selected {option_text} in {element_id}")
        return True
    except Exception as e:
        print(f"Could not locate element with visible text: {option_text} in {element_id}. Error: {e}")
        return False

# List to store scraped data
scraped_data = []

# Extract blood groups
blood_groups = get_dropdown_options("dpBloodGroup")
print("Blood Groups:", blood_groups)

# Iterate over the blood groups
for blood_group in blood_groups:
    select_dropdown_option("dpBloodGroup", blood_group)
    time.sleep(1)

    # Extract countries based on the selected blood group
    countries = get_dropdown_options("dpCountry")
    print(f"Countries for Blood Group {blood_group}:", countries)

    for country in countries:
        if country == "INDIA":  # Only process INDIA
            select_dropdown_option("dpCountry", country)
            time.sleep(1)

            # Extract states based on the selected country
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "dpState")))
            states = get_dropdown_options("dpState")
            print(f"States for Country {country}:", states)

            for state in states:
                select_dropdown_option("dpState", state)
                time.sleep(1)

                # Extract districts based on the selected state
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "dpDistrict")))
                districts = get_dropdown_options("dpDistrict")
                print(f"Districts for State {state}:", districts)

                for district in districts:
                    select_dropdown_option("dpDistrict", district)
                    time.sleep(1)

                    # Extract cities based on the selected district
                    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "dpCity")))
                    cities = get_dropdown_options("dpCity")
                    print(f"Cities for District {district}:", cities)

                    for city in cities:
                        if not select_dropdown_option("dpCity", city):
                            continue  # Skip this city if not found
                        time.sleep(1)

                        # Now click the search button and scrape the data
                        search_button = driver.find_element(By.ID, "btnSearchDonor")
                        search_button.click()
                        time.sleep(1)  # Wait for search results to load

                        # Scrape the table data here
                        try:
                            table = driver.find_element(By.ID, "dgBloodDonorResults")
                            rows = table.find_elements(By.TAG_NAME, "tr")

                            for row in rows[1:]:  # Skip the header row
                                cols = row.find_elements(By.TAG_NAME, "td")
                                if len(cols) >= 3:
                                    name = cols[0].text
                                    mobile_no = cols[2].text  # Corrected to get the mobile number from the 3rd column
                                    scraped_data.append({
                                        'Blood Group': blood_group,
                                        'Country': country,
                                        'State': state,
                                        'District': district,
                                        'City': city,
                                        'Name': name,
                                        'Mobile No.': mobile_no
                                    })

                        except Exception as e:
                            print(f"Error scraping data for {city}, {district}, {state}: {e}")

                        # After scraping the current city, continue to the next one
                        # ...

# Close the browser session when done
driver.quit()

# Save the scraped data to a CSV file
df = pd.DataFrame(scraped_data)
df.to_csv('blood_donor_data_india.csv', index=False)

print("Dropdown mapping and data scraping completed.")
print(f"Data saved to 'blood_donor_data_india.csv'.")