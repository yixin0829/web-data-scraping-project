# The website we're scraping data from is: https://ags.aer.ca/data-maps-models/digital-data
from bs4 import BeautifulSoup
import requests


source = requests.get('https://ags.aer.ca/data-maps-models/digital-data')
# Extract the html text in source (i.e. the website we try to scrap data from)
content = source.content

# Creating a soup object based on the content of the source 
# Note: using lxml’s HTML parser - very fast. Or can use Python's html.parser - a bit slower
soup = BeautifulSoup(content, features='lxml')

# Narrowing down the searching scope
result = soup.find(class_ = "list-results row")
# html black that contains result of year & id, title, and author data
containers = result.find_all(class_ = "list-item clearfix")

filename = "date_title_author.csv"
f = open(filename, "w")

headers = "DataID,Publication date,Titile,Author#1,Author#2,Author#3,Author#4\n"

f.write(headers)


for container in containers:
    publication_date = container.find(class_ = "pub-date").get_text().strip()
    dataID = container.find("li").get_text().strip()
    title = container.find("a").get_text()
    
    author_block = container.find(class_ = "author-list")
    # authors contains all the a tags html text 
    authors = author_block.find_all("a")
    
    """
    # Declare a list for author's name
    author_list = []
    for author in authors:
            author_list.append(author.get_text())
    # Join the list into one string separated by "|"
    author_str = "|".join(author_list)
    """

    # write into the csv file every iteration
    # Note: use replace() to replace the "," inside author_list
    f.write(dataID + "," + publication_date.replace(",", " ") + "," + title.replace(",", " "))
    for author in authors:
        f.write("," + author.get_text().replace(",", " "))
    f.write("\n")

f.close()

f = open("key_words.csv", "w")
f.write("Data ID,Key word#1,Key word#2,Key word#3,Key word#4,Key word#5,Key word#6,Key word#7,Key word#8,Key word#9,Key word#10,Key word#11,Key word#12\n")

# Extract the keywords for each article (needs nested http requests)
# Issue: take too much time ~15 min
iteration = 0 # Count current # of loops and output to terminal
for container in containers:
    dataID = container.find("li").get_text().strip()
    a_tag = container.find("a")
    link = a_tag.attrs['href']
    source = requests.get('https://ags.aer.ca/'+ link)
    content = source.content
    soup = BeautifulSoup(content, 'lxml')
    key_words_block = soup.find_all(class_ = "keywords inline")[1]
    # Find all the li tags exclude the first one
    key_words = key_words_block.find_all("li")[1:]
    f.write(dataID)

    # Write the keys words into .csv file
    for key_word in key_words:
        f.write("," + key_word.get_text())
    f.write("\n")

    # Terminal output for debugging
    print("Extraction successful" + str(iteration))
    iteration += 1

f.close()



