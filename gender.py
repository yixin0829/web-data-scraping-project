import pandas as pd
import numpy as np
import requests
import json

def genderize_api_connect(first_name):
    try:
        url = 'https://api.genderize.io/?name={}'.format(first_name)
        response = requests.get(url,timeout=10)
        content = json.loads(response.content)
        print("Got content: "+first_name)
    except:
        print("Timed out.")
        content = None
    return content

def author_gender(all_authors, threshold=0.6):
    for key, value in all_authors.items():
        # Ensure the author being evaluated has not been enriched using the API — this avoids unnecessary API calls
        if 'gender' not in value:
            try:
               # Retrieve the probability of the gender prediction of the author 
               # and compare it to the threshold set in line 11.
                result = genderize_api_connect(value['first_name'])
                if result['probability'] > threshold:
                    # Add the gender to the author dictionary object and ensure that it is capitalized.
                    value['gender'] = result['gender'].capitalize()
                    # Handle exceptions, specifically if no gender is returned from the API. 
                    # This case is handled by assigning the gender as “Unknown”.
                else:
                    value['gender'] = "Unknown"
            except (KeyError,TypeError):
                value['gender'] = "Unknown"
            
    return all_authors

def store_dict(data,all_authors):
    for i in range(1,12):
        for j in range(1434):
            Str = str(data['Author#'+str(i)][j])
            Str = Str.strip()
            full_name = Str
            if Str != "NaN":
                Str = Str.split(' ', 1)[0]
                if full_name not in all_authors:
                    all_authors[full_name] = {'first_name':Str}




data = pd.read_csv('date_title_author.csv') 
all_authors = {}

store_dict(data,all_authors)
print("successfully stored")
author_gender(all_authors)


print("Start writing into csv:")
filename = "genders.csv"
f = open(filename,"w")
headers = "Author,First name,Predicted gender\n"
f.write(headers)
for key,value in all_authors.items():
    val_array = list(value.values())
    print(val_array)
    f.write(key+","+val_array[0]+","+val_array[1])
    f.write("\n")
f.close()

