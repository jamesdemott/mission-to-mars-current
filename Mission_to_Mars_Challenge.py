#!/usr/bin/env python
# coding: utf-8

# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd

# Path to chromedriver
#get_ipython().system('which chromedriver')


# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path)


# ### Visit the NASA Mars News Site

# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('ul.item_list li.slide')


slide_elem.find("div", class_='content_title')


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title



# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p


# ### JPL Space Images Featured Image

# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()

# Find the more info button and click that
browser.is_element_present_by_text('more info', wait_time=1)
more_info_elem = browser.links.find_by_partial_text('more info')
more_info_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# find the relative image url
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel


# Use the base url to create an absolute url
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url


# ### Mars Facts


df = pd.read_html('http://space-facts.com/mars/')[0]

df.head()


df.columns=['Description', 'Mars']
df.set_index('Description', inplace=True)
df


df.to_html()


# ### Mars Weather

# In[18]:


# Visit the weather website
url = 'https://mars.nasa.gov/insight/weather/'
browser.visit(url)



# Parse the data
html = browser.html
weather_soup = soup(html, 'html.parser')


# Scrape the Daily Weather Report table
weather_table = weather_soup.find('table', class_='mb_table')
print(weather_table.prettify())


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)

hemisphere_image_urls = []

# First, get a list of all of the hemispheres
links = browser.find_by_css("a.product-item h3")

# Next, loop through those links, click the link, find the sample anchor, return the href
for i in range(len(links)):
    hemisphere = {}
    
    # We have to find the elements on each loop to avoid a stale element exception
    browser.find_by_css("a.product-item h3")[i].click()

    # Next, we find the Sample image anchor tag and extract the href
    sample_elem = browser.links.find_by_text('Sample').first
    hemisphere['img_url'] = sample_elem['href']
    
    # Get Hemisphere title
    hemisphere['title'] = browser.find_by_css("h2.title").text
    
    # Append hemisphere object to list
    hemisphere_image_urls.append(hemisphere)
    
    # Finally, we navigate backwards
    browser.back()
    
print(hemisphere_image_urls)

# 5. Quit the browser
browser.quit()