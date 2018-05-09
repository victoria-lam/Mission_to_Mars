from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import time

# create path to chromedriver
def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

# scrape Mars data
def scrape():
    browser = init_browser()

    mars = {}
    
   ##NASA Mars News
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    
    mars["news_title"] = soup.find("div", class_="content_title").text
    mars["news_p"] = soup.find("div", class_="rollover_description_inner").text

    
   ##JPL Mars Space Images - Featured Image
    pic_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(pic_url)
    
    browser.click_link_by_partial_text("FULL IMAGE")
    time.sleep(5)
    
    browser.click_link_by_partial_text("more info")

    pic_html = browser.html
    pic_soup = BeautifulSoup(pic_html, "html.parser")
    base_url = "https://www.jpl.nasa.gov"
    image_url = pic_soup.find("figure", class_="lede").a["href"]
    mars["featured_image_url"] = base_url + image_url
    
    
   ##Mars weather
    tweet_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(tweet_url)
    tweet_html = browser.html
    tweet_soup = BeautifulSoup(tweet_html, "html.parser")
    
    mars["mars_weather"] = tweet_soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    
    
   ##Mars facts
    table = pd.read_html("https://space-facts.com/mars/")
    df = table[0]
    df.columns = ["Description", "Value"]
    mars["facts_table"] = df.to_html()
    
    
   ##Mars hemispheres
    hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemi_url)
    hemi_html = browser.html
    hemi_soup = BeautifulSoup(hemi_html, "html.parser")
    
    cerberus= "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg"
    schiaparelli = "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg"
    syrtis_major = "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg"
    valles_marineris = "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg"
    img_urls = [cerberus, schiaparelli, syrtis_major, valles_marineris]
    
    img_titles = []
    titles = hemi_soup.find_all("h3")

    for title in titles:
        img_titles.append(title.get_text())
    
    mars["hemisphere_image_urls"] = [{"title": img_titles, "img_url": img_urls} for img_titles, img_urls in zip(img_titles, img_urls)]
      
    return mars

   
