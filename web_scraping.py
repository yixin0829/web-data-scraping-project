from flask import Flask, render_template
from bs4 import BeautifulSoup
import requests

source = requests.get('https://ags.aer.ca/data-maps-models/digital-data').text

soup = BeautifulSoup(source, features='lxml')

print(soup)