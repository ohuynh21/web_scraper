# import module 
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd
from bs4 import BeautifulSoup

import time 

# Create the webdriver object. 
# the chromedriver is present in the root directory. 
driver = webdriver.Chrome()

# login
driver.get("https://cape.ucsd.edu/") 
driver.implicitly_wait(0.5)
search_button = driver.find_element(by = By.CSS_SELECTOR, value = 'input.button.primary[type="submit"]')
search_button.click()

driver.find_element(By.ID, "ssousername").clear()
driver.find_element(By.ID, "ssousername").send_keys("REDACTED")
driver.find_element(By.ID, "ssopassword").clear()
driver.find_element(By.ID, "ssopassword").send_keys("REDACTED")

button = driver.find_element(By.CLASS_NAME, "btn-primary")
button.click()

# wait for Duo Authentication
time.sleep(20)


# for each class in the dropdown menu, scrape the table and convert it into a pandas df
dropdown_element = driver.find_element(By.ID, "ContentPlaceHolder1_ddlDepartments")
dropdown = Select(dropdown_element)
options = dropdown.options

df_list = []

for option in options:
    option_text = option.text
    print(option_text)
    dropdown.select_by_visible_text(option_text)
    button = driver.find_element(by = By.ID, value = 'ContentPlaceHolder1_btnSubmit')
    button.click()
    
    # wait for page to load
    time.sleep(5)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    # try to scrape the table
    try:
        table = soup.find('table', {'id': 'ContentPlaceHolder1_gvCAPEs'})
        table_data = []
        for row in table.find_all('tr'):
            row_data = []
            for cell in row.find_all(['th', 'td']):
                row_data.append(cell.get_text(strip=True))
            table_data.append(row_data)

        # convert the extracted data into a Pandas DataFrame
        df = pd.DataFrame(table_data[1:], columns=table_data[0])
        print(df.head(), df.shape)
        df_list.append(df)

    except:
        print('An Error Has Occurred')

# merge the dataframes for each class together and export it as a csv
final_df = pd.concat(df_list)
final_df.to_csv('output.csv', index = False)