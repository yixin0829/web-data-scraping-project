# The website we're scraping data from is: https://ags.aer.ca/data-maps-models/digital-data
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np
import requests
import nltk

source = requests.get('https://ags.aer.ca/data-maps-models/digital-data')
content = source.content

# Creating a soup object based on the content of the source
soup = BeautifulSoup(content, features='lxml')

# Narrowing down the searching scope
result = soup.find(class_ = "list-results row")
# html black that contains result of year & id, title, and author data
result_rows = result.find_all(class_ = "unstyled item-content")
# html block that contains the publication date data
date_blocks = result.find_all(class_ = "pub-date")

# Extracting all dates, titles, and author names
# Append the data to separate lists
year_list = []
id_list = []
for element in result_rows:
    li_tag = element.find("li")
    year_list.append(li_tag.get_text()[13:17])
    id_list.append(li_tag.get_text()[18:22])

publication_date_list = []
for element in date_blocks:
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
# Issue: take too much time ~25 min
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

# Visualizing the # of data sets being posted every year from 2002 to 2019
num_bins = 18
n, bins, patches = plt.hist(year_list, num_bins, facecolor='blue', alpha=0.5)
plt.xlabel('Years')
plt.ylabel('# of Sets')
plt.title(r'Number of Published Data Sets from 2002 - 2019')
plt.subplots_adjust(left=0.15)
plt.show()

# nltk.download('punkt')
# def graph():
#   tokens = nltk.tokenize.word_tokenize(title_list)
#   fd = nltk.FreqDist(tokens)
#   fd_t10 = fd.most_common(10)
#   fd.plot(30,cumulative=False)

# graph()
