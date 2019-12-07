#!/usr/bin/env python
# coding: utf-8

# # Mission to Mars

# In[33]:


import pandas as pd
import requests
from splinter import Browser
from bs4 import BeautifulSoup


# In[34]:


# URL of page to be scraped
url = "https://mars.nasa.gov/news/"


# In[40]:


# Retrieve page with the requests module
response = requests.get(url)


# In[41]:


# Create BeautifulSoup object; parse with 'html.parser'
soup = BeautifulSoup(response.text,"lxml")
print(soup.prettify())


# # Web Scraping

# ## NASA Mars News

# In[42]:


results = soup.find_all('div', class_='slide')


# In[46]:


#Retrieve titles and paragraphs of the most recent news
news_titles = []
news_ps = []

for result in results:
    news_title = result.find('div', class_='content_title').a.text
    news_p = result.find('div', class_='rollover_description_inner').text
    
    news_titles.append(news_title)
    news_ps.append(news_p)
    
    print("----------------")
    print(news_title)
    print(news_p)


# In[ ]:





# ## JPL Mars Space Images - Featured Image

# In[50]:


url_img = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"


# In[51]:


executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


# In[52]:


# Use splinter to navigate the site and find the image url for the current Featured Mars Image
browser.visit(url_img)
html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# In[54]:


featured_image_url = soup.find('img', title='Indus Vallis')['src']
featured_image_url


# ## Mars Weather

# In[55]:


url_weather = "https://twitter.com/marswxreport?lang=en"


# In[56]:


response_weather = requests.get(url_weather)
soup = BeautifulSoup(response_weather.text, "html.parser")


# In[60]:


results = soup.find_all('p', class_="TweetTextSize")


# In[62]:


# Extract weather data and store in a list
mars_weather = []
for result in results:
    mars_weather.append(result.text)
    
    print("------------")
    print(result.text)


# ## Mars Facts

# In[63]:


url_facts = "https://space-facts.com/mars/"


# In[103]:


# Use Pandas Scraping
mars_facts = pd.read_html(url_facts)
mars_facts


# In[114]:


mars_facts_df = mars_facts[0]
mars_facts_df.columns=['Measure of','Value']
mars_facts_df = mars_facts_df.set_index('Measure of')
mars_facts_df


# In[116]:


# dataframe to html
html_table = mars_facts_df.to_html()
html_table


# In[119]:


html_table = html_table.replace("\n","")
html_table


# ## Mars Hemispheres

# In[120]:


url_hemisphere = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"


# In[121]:


response = requests.get(url_hemisphere)
soup = BeautifulSoup(response.text, "html.parser")


# In[125]:


results = soup.find_all('div', class_="item")


# In[130]:


#Find urls for high resolution images and store urls in a list
url_high_resolution = []
for result in results:
    url_high_resolution.append(result.a['href'])
url_high_resolution


# In[163]:


# image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name
hemisphere_image_urls = []

for i in url_high_resolution:
    response = requests.get(f"https://astrogeology.usgs.gov{i}")
    soup = BeautifulSoup(response.text, "html.parser")
    
    title = soup.find('h2', class_='title').text
    img_url = soup.find('li').a['href']
    hemisphere_image_urls.append({"title":title,"img_url":img_url})
    print("-------------")
    print(title)
    print(img_url)


# In[164]:


hemisphere_image_urls


# # MongoDB and Flask Application

# In[ ]:




