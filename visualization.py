# The website we're scraping data from is: https://ags.aer.ca/data-maps-models/digital-data
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np
import requests
from nltk.probability import FreqDist

source = requests.get('https://ags.aer.ca/data-maps-models/digital-data')
content = source.content

# Creating a soup object based on the content of the source
soup = BeautifulSoup(content, features='lxml')

# Narrowing down the searching scope
result = soup.find(class_ = "list-results row")
# html black that contains result of year & id, title, and author data
result_blocks = result.find_all(class_ = "unstyled item-content")
# html block that contains the publication date data
date_blocks = result.find_all(class_ = "pub-date")
# html list block that contains author data
author_blocks = result.find_all(class_ = "author-list")


# Extracting all dates, titles, and author names
# Append the data to separate lists
year_list = []
for element in result_blocks:
    li_tag = element.find("li")
    year_list.append(li_tag.get_text()[13:17])

publication_date_list = []
for element in date_blocks:
    # strip method remove the spaces on the right/leftof the dates
    publication_date_list.append(element.get_text().strip()) 

title_list = []
for element in result_blocks:
    a_tag = element.find("a")
    title_list.append(a_tag.get_text())

author_list = []
for element in author_blocks:
    a_tag = element.find_all("a")
    # Append the author names into the list depending on the lenth of the a_tag list (i.e. how many authors)
    for x in range(len(a_tag)):
        author_list.append(a_tag[x].get_text())


# Extract the abstract for each article (needs a second get request)
# Issue: take too much time ~25 min
"""
abstract_list = []
for element in result_blocks:
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
# print(title_list)
# print(author_list)
# print(publication_date_list)
# print(abstract_list)

# Visualizing the # of data sets being posted every year from 2002 to 2019
num_bins = 18
n, bins, patches = plt.hist(year_list, num_bins, facecolor='blue', alpha=0.5)
plt.xlabel('Years')
plt.ylabel('# of Sets')
plt.title(r'Number of Published Data Sets from 2002 - 2019')



# Creating a new plot for visualizing the popular publishers
plt.figure()
# Declaring fdist object of class FreqDist
fdist = FreqDist()
for word in author_list:
    fdist[word.lower()] += 1

plt.title(r'Number of Published Data Sets from Different Publishers')
fdist.plot(20)



