# PREDOC.org Scraping Code

# Importing packages
from bs4 import BeautifulSoup 
import requests 
import pandas as pd
import lxml

# Getting HTML text
html_text = requests.get('https://www.predoc.org/opportunities',).text
soup = BeautifulSoup(html_text, 'lxml')

# Creating list of job site sections using CSS selector (complex class attributes)
openings = soup.select('article.all.sorted')

# Defining function to extract job info data from p-tag text
def extract_job_info(p_tag):
    data = {}
    current_label = None

    for element in p_tag.contents:
        # .contents returns all the direct children of an html tag (from B.S.)
        if element.name == "strong":
            current_label = element.get_text(strip=True).rstrip(":")
            data[current_label] = ""
        elif element.name == "br":
            current_label = None
        elif current_label:
            data[current_label] += element.get_text(strip=True) + " "
    return data

# Empty list to hold job posting dictionaries
posting_data_list = []

# Creating job posting dictionaries
for job in openings:
    job_info = {}
    job_dictionary = []

   # ----- Simple Data -----
   # Getting job title
    job_title_h2 = job.find('h2')
    job_title = job_title_h2.find('a').text.strip() if job_title_h2 else None
    print (job_title)
    
    # Getting job link
    job_link_tag = job.find("a", href=True)
    job_link = job_link_tag["href"] if job_link_tag else None
    print(job_link)

    # ----- Complex Variables -----
    # Getting job text information
    p_tag = job.find("p")
    if p_tag:
        job_text_info = extract_job_info(p_tag)
    else:
        job_text_info = {}
    print(job_text_info)

    # ----- Combining in final dictionary -----
    # Adding simple variables to dictionaries 
    job_dictionary = { 
        'Job Title' : job_title,
        'Link' : job_link
    }
    # Updating dictionary with complex text data dictionary 
    job_dictionary.update(job_text_info)

    # Adding dictionary to list for data frame
    posting_data_list.append(job_dictionary)

# Saving collected list of dictionaries into a dataframe and CSV file
df = pd.DataFrame(posting_data_list)
print(df.head())
df.to_csv('predoc_job_raw_data.csv')