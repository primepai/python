#GTA area ctv news updates

import requests
from bs4 import BeautifulSoup 

page = requests.get('https://toronto.ctvnews.ca/more/local-news')

# Create a BeautifulSoup object
soup = BeautifulSoup(page.text, 'html.parser')

headline = soup.find_all(class_='teaserTitle')


#append news
title_sum=[]
for line in headline:
    for a in line.find_all('a',href=True):
        title_sum.append(a['href'])

for j in range(1,len(title_sum)):
    new_string=title_sum[j].replace('-'," ").replace('/',"")
    if 'video?' not in new_string:
        print(new_string[0:(len(new_string)-10)]+'.')
        print("")

 # partial sample output
'''
hamilton police officer sentenced to 12 years for bribery cocaine trafficking.

police identify victim of fatal shooting in yorkville.

roseanne yanked from ctv lineup and streaming platforms.

red sox beat blue jays 8 3.

police release getaway route used by mississauga restaurant bombers.

toronto police investigating music video that takes aim at ttc system.

maple leafs winger zack hyman writes children s book about imagination.

ndp sticks with brampton candidate photographed holding anti police sign.
'''
