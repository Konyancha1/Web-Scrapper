# Import libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd
from keep import keep_alive

keep_alive()

# Create instance of driver
driver = webdriver.Chrome("C:\\Users\\user\\Talent Network Project\\Driver\\chromedriver.exe")
driver.maximize_window() 
driver.minimize_window()  
driver.maximize_window()  
driver.switch_to.window(driver.current_window_handle)
driver.implicitly_wait(10)
driver.get("https://linkedin.com/uas/login")

# Logging in to LinkedIn
username = driver.find_element(By.ID, "username")
username.send_keys("nick@braveventurelabs.com")
time.sleep(0.5)
passWord = driver.find_element(By.ID, "password")
passWord.send_keys("rWF7mWE9vq")
time.sleep(0.5)
driver.find_element(By.XPATH, "//button[@type='submit']").click()
time.sleep(3)

def getTalent():
    links = []
    names = []
    profiles = []
    companies = []
    titles = []
    # Iterate throught Google page containing linkedin links 
    # and run the function to extract data from each of the links
    for page in range(1, 3, 1):
        talent_page = "https://www.linkedin.com/search/results/PEOPLE/?currentCompany=%5B%2210910136%22%2C%229244517%22%2C%2211356076%22%2C%222789728%22%2C%2247206%22%5D&geoUrn=%5B%22100710459%22%5D&keywords=financial%20reporting&origin=FACETED_SEARCH&page=" +str(page)
        driver.get(talent_page)
        time.sleep(60)

        people = driver.find_element(By.CLASS_NAME, 'search-results-container')
        people_list= people.find_elements(By.CSS_SELECTOR, '.reusable-search__result-container')
        for person in people_list:
            all_links = person.find_elements(By.TAG_NAME, 'a')
            for a in all_links:
                if str(a.get_attribute('href')).startswith("https://www.linkedin.com/in") and a.get_attribute('href') not in links: 
                    links.append(a.get_attribute('href'))
                else:
                    pass

            # scroll down
            driver.execute_script("arguments[0].scrollIntoView();", person)
        
        print(f'Collecting the links in the page: {page+1}')
    print("Found", str(len(links)), "links")
    print("Starting to scrape profiles now...")
    
    global linkedin_url
    for linkedin_url in links:
        driver.get(linkedin_url)
        time.sleep(30)
        # Store page source code and create soup object for data extraction
        src = driver.page_source
        soup = BeautifulSoup(src, 'lxml')
        try:
            if links.index(linkedin_url) % 10 == 0:
                time.sleep(900)
        except:
            pass
        profiles.append(linkedin_url)
        try:
            # Extracting the Name
            global name
            profile_name = soup.find('div', {'class': 'pv-text-details__left-panel'})
            linkedin_name = profile_name.find('h1')
            name = linkedin_name.get_text().strip()
            names.append(name) 
        except:
            names.append("Not found")
        try:
            # Extracting the Company Name
            global company
            company_name = soup.find('li', {'class': 'pv-text-details__right-panel-item'})
            linkedin_company_name = company_name.find('div')
            company = linkedin_company_name.get_text().strip()
            companies.append(company)
        except:
            companies.append("Not found")
            # Extracting the Title
        try:
            global title
            title_name = soup.find('div', {'class': 'pv-text-details__left-panel'})
            linkedin_title = title_name.find('div', {'class': 'text-body-medium break-words'})
            title = linkedin_title.get_text().strip()
            titles.append(title)
        except:
            titles.append("Not found")

    df = pd.DataFrame(list(zip(names, titles, companies, profiles)),
                    columns =['names', 'roles', 'companies', 'profile'])
    df.to_csv('talent_community_4.csv', index=False)
    print("Done")

getTalent()

# Closes the browser and shuts down the driver
driver.quit()
