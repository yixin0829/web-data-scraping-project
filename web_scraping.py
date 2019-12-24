from flask import Flask, render_template
from bs4 import BeautifulSoup
import requests

source = requests.get('https://ags.aer.ca/data-maps-models/digital-data')
content = source.content

# Creating a soup object
soup = BeautifulSoup(content, features='lxml')

result = soup.find(class_ = "list-results row")
result_rows = result.find_all(class_ = "unstyled item-content")

# Extracting all the dates data and append them to result_list
result_list = []
for element in result_rows:
    li_tag = element.find("li")
    result_list.append(li_tag.get_text())

print(result_list)


