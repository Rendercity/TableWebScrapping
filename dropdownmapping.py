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

# Extract Blood Groups
blood_groups = get_dropdown_options("dpBloodGroup")
print("blood_groups =", blood_groups)

# Extract Countries
countries = get_dropdown_options("dpCountry")
print("countries =", countries)

# Initialize dictionaries for states, districts, and cities
states = {}
districts = {}
cities = {}

# Extract States
for country in countries:
    Select(driver.find_element(By.ID, "dpCountry")).select_by_visible_text(country)
    time.sleep(3)  # Give time to load the next dropdown
    states[country] = get_dropdown_options("dpState")

    # Extract Districts
    districts[country] = {}
    for state in states[country]:
        Select(driver.find_element(By.ID, "dpState")).select_by_visible_text(state)
        time.sleep(3)
        districts[country][state] = get_dropdown_options("dpDistrict")

        # Extract Cities
        cities[country] = {}
        cities[country][state] = {}
        for district in districts[country][state]:
            Select(driver.find_element(By.ID, "dpDistrict")).select_by_visible_text(district)
            time.sleep(3)
            cities[country][state][district] = get_dropdown_options("dpCity")

# Close the browser session when done
driver.quit()

# Print formatted details
print("\nblood_groups =", blood_groups)
print("\ncountries =", countries)
print("\nstates =", states)
print("\ndistricts =", districts)
print("\ncities =", cities)

# You can redirect the output to a file if needed
with open('dropdown_details.txt', 'w') as file:
    file.write("blood_groups = " + str(blood_groups) + "\n")
    file.write("countries = " + str(countries) + "\n")
    file.write("states = " + str(states) + "\n")
    file.write("districts = " + str(districts) + "\n")
    file.write("cities = " + str(cities) + "\n")

print("Dropdown details have been gathered and saved to 'dropdown_details.txt'.")