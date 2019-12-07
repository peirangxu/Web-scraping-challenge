import pandas as pd
import requests
from splinter import Browser
from bs4 import BeautifulSoup
import time

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    mars_data = {}

    #mars news
    url = "https://mars.nasa.gov/news/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text,"html.parser")

    results = soup.find_all('div', class_='slide')

    for result in results:
        news_title = result.find('div', class_='content_title').a.text.strip()
        news_p = result.find('div', class_='rollover_description_inner').text.strip()
    
        mars_data["news_title"] = news_title
        mars_data["news_p"] = news_p

    #JPL Mars Space Images - Featured Image
    browser = init_browser()

    url_img = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_img)

    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    featured_image_url = soup.find('img', title='Indus Vallis')['src']
    mars_data["featured_image_url"] = f"https://www.jpl.nasa.gov{featured_image_url}"

    browser.quit()

    #Mars Weather
    url_weather = "https://twitter.com/marswxreport?lang=en"

    response_weather = requests.get(url_weather)
    soup = BeautifulSoup(response_weather.text, "html.parser")

    results = soup.find_all('p', class_="TweetTextSize")

    for result in results:
        mars_data["mars_weather"] = result.text
    
    #Mars Facts
    url_facts = "https://space-facts.com/mars/"

    mars_facts = pd.read_html(url_facts)
    mars_facts_df = mars_facts[0]
    mars_facts_df.columns=['Measure of','Value']
    mars_facts_df = mars_facts_df.set_index('Measure of')
    html_table = mars_facts_df.to_html()
    html_table = html_table.replace("\n","")

    mars_data["mars_facts"] = html_table

    #Mars Hemispheres
    url_hemisphere = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    response = requests.get(url_hemisphere)
    soup = BeautifulSoup(response.text, "html.parser")

    results = soup.find_all('div', class_="item")

    url_high_resolution = []
    for result in results:
        url_high_resolution.append(result.a['href'])

    for i in url_high_resolution:
        response = requests.get(f"https://astrogeology.usgs.gov{i}")
        soup = BeautifulSoup(response.text, "html.parser")
    
        title = soup.find('h2', class_='title').text
        img_url = soup.find('li').a['href']

        mars_data["hemisphere_image_title"] = title
        mars_data["hemisphere_image_url"] = img_url

    # Return results
    return mars_data



