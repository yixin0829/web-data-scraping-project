from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np
import requests

source = requests.get('https://ags.aer.ca/data-maps-models/digital-data')
content = source.content

# Creating a soup object
soup = BeautifulSoup(content, features='lxml')
result = soup.find(class_ = "list-results row")
result_rows = result.find_all(class_ = "unstyled item-content")
date_elements = result.find_all(class_ = "pub-date")

# Extracting all dates, titles, and author names
# Append the data to separate lists
year_list = []
id_list = []
for element in result_rows:
    li_tag = element.find("li")
    year_list.append(li_tag.get_text()[13:17])
    id_list.append(li_tag.get_text()[18:22])

publication_date_list = []
for element in date_elements:
    # strip method remove the spaces on the right/leftof the dates
    publication_date_list.append(element.get_text().strip()) 

title_list = []
for element in result_rows:
    a_tag = element.find("a")
    title_list.append(a_tag.get_text())

author_list = []
for element in result_rows:
    a_tag = element.find_all("a")[1]
    author_list.append(a_tag.get_text())

# Extract the abstract for each article (needs a second get request)
"""
abstract_list = []
for element in result_rows:
    a_tag = element.find("a")
    link = a_tag.attrs['href']
    article = requests.get('https://ags.aer.ca/'+ link)
    content = article.content
    soup = BeautifulSoup(content, 'lxml')
    summary = soup.find(id = "summary")
    abstract = summary.find("p")
    #print(abstract.get_text())
    abstract_list.append(abstract.get_text())
    #print("extraction succeed")
    
"""   

# print(year_list)
# print(id_list)
# print(title_list)
# print(author_list)
# print(publication_date_list)
# print(abstract_list)

num_bins = 18
n, bins, patches = plt.hist(year_list, num_bins, facecolor='blue', alpha=0.5)
plt.xlabel('Years')
plt.ylabel('# of Sets')
plt.title(r'Number of Published Data Sets from 2002 - 2019')
plt.subplots_adjust(left=0.15)
plt.show()
