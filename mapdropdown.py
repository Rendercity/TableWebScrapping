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

# Function to extract options from a dropdown
def get_dropdown_options(element_id):
    dropdown = Select(driver.find_element(By.ID, element_id))
    options = [option.text for option in dropdown.options if option.text != 'Select']
    return options

# Extract blood groups
blood_groups = get_dropdown_options("dpBloodGroup")
print("Blood Groups:", blood_groups)

# Select a blood group (this can be automated if you loop over them)
for blood_group in blood_groups:
    Select(driver.find_element(By.ID, "dpBloodGroup")).select_by_visible_text(blood_group)
    time.sleep(3)  # Give time to load the next dropdown

    # Extract countries based on the selected blood group
    countries = get_dropdown_options("dpCountry")
    print(f"Countries for Blood Group {blood_group}:", countries)

    for country in countries:
        Select(driver.find_element(By.ID, "dpCountry")).select_by_visible_text(country)
        time.sleep(3)

        # Extract states based on the selected country
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "dpState")))
        states = get_dropdown_options("dpState")
        print(f"States for Country {country}:", states)

        for state in states:
            Select(driver.find_element(By.ID, "dpState")).select_by_visible_text(state)
            time.sleep(3)

            # Extract districts based on the selected state
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "dpDistrict")))
            districts = get_dropdown_options("dpDistrict")
            print(f"Districts for State {state}:", districts)

            for district in districts:
                Select(driver.find_element(By.ID, "dpDistrict")).select_by_visible_text(district)
                time.sleep(3)

                # Extract cities based on the selected district
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "dpCity")))
                cities = get_dropdown_options("dpCity")
                print(f"Cities for District {district}:", cities)

                for city in cities:
                    Select(driver.find_element(By.ID, "dpCity")).select_by_visible_text(city)
                    time.sleep(3)

                    # Now you can click the search button and scrape the data
                    search_button = driver.find_element(By.ID, "btnSearchDonor")
                    search_button.click()
                    time.sleep(3)  # Wait for search results to load

                    # Scrape the data here (like your previous code)

                    # After scraping the current city, continue to the next one
                    # ...

# Close the browser session when done
driver.quit()

print("Dropdown mapping completed.")