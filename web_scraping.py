from bs4 import BeautifulSoup
import requests

source = requests.get('https://ags.aer.ca/data-maps-models/digital-data')
content = source.content

# Creating a soup object
soup = BeautifulSoup(content, features='lxml')
result = soup.find(class_ = "list-results row")
result_rows = result.find_all(class_ = "unstyled item-content")

# Extracting all dates, titles, and author names
# Append the data to separate lists
date_list = []
for element in result_rows:
    li_tag = element.find("li")
    date_list.append(li_tag.get_text())

title_list = []
for element in result_rows:
    a_tag = element.find("a")
    title_list.append(a_tag.get_text())

author_list = []
for element in result_rows:
    a_tag = element.find_all("a")[1]
    author_list.append(a_tag.get_text())

# print(date_list)
# print(title_list)
# print(author_list)


