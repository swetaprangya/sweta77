from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd

# NASA Exoplanet URL
START_URL = "https://exoplanets.nasa.gov/exoplanet-catalog/"

# Webdriver
browser = webdriver.Chrome()
browser.get(START_URL)

time.sleep(10)

new_planets_data = []

def scrape_more_data(hyperlink):
    print(hyperlink)
    try:
        page=requests.get(hyperlink)
        soup=BeautifulSoup(page.content,"html.parser")
        temp_list=[]
        for tr_tag in soup.find_all("tr",attrs={"class":"fact_row"}):
            td_tags=tr_tag.find_all("td")
            for td_tag in td_tags :
                try:
                    temp_list.append(td_tags.find_all("div",attrs={"class","value"})[0].contents[0])
                except:
                    temp_list.append("")
        new_planets_data.append(temp_list)
    except:
        time.sleep(10)
        scrape_more_data(hyperlink)        

    
    ## ADD CODE HERE ##







planet_df_1 = pd.read_csv("updated_scraped_data.csv")

# Call method
for index, row in planet_df_1.iterrows():
    print(row["hyperlink"])
    scrape_more_data(row["hyperlink"])

     ## ADD CODE HERE ##
    

     # Call scrape_more_data(<hyperlink>)

    print(f"Data Scraping at hyperlink {index+1} completed")

print(new_planets_data)

# Remove '\n' character from the scraped data
scraped_data = []

for row in new_planets_data:

    replaced = []
    for el in row: 
        el = el.replace("\n", "") 
        replaced.append(el)
    
    ## ADD CODE HERE ##


    
    scraped_data.append(replaced)

print(scraped_data)

headers = ["planet_type","discovery_date", "mass", "planet_radius", "orbital_radius", "orbital_period", "eccentricity", "detection_method"]

new_planet_df_1 = pd.DataFrame(scraped_data,columns = headers)

# Convert to CSV
new_planet_df_1.to_csv('new_scraped_data.csv', index=True, index_label="id")
