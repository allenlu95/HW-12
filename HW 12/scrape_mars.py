#!/usr/bin/env python
# coding: utf-8

from splinter import Browser
from bs4 import BeautifulSoup as bs

def scrape():
    mars_dict = {}

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    
    nasa_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(nasa_url)
    html = browser.html
    soup = bs(html, "html.parser")
    
    mars_dict['news_title'] = soup.find("div", class_="content_title").get_text()
    mars_dict['news_teaser'] = soup.find("div", class_="article_teaser_body").get_text()

    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)
    browser.click_link_by_partial_text('FULL')
    html = browser.html
    soup = bs(html, "html.parser")
    
    featured_image_src = soup.find(class_="carousel_item")['style']
    featured_image_src = featured_image_src.strip("background-image: url('")
    featured_image_src = featured_image_src.strip("');")
    featured_image_url = "https://www.jpl.nasa.gov" + featured_image_src
    
    mars_dict['featured_img'] = featured_image_url

    twit_url = "https://twitter.com/MarsWxReport"
    browser.visit(twit_url)
    html = browser.html
    soup = bs(html, "html.parser")

    mars_dict['weather'] = soup.find("p", class_="tweet-text").get_text()

    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    html = browser.html
    soup = bs(html, "html.parser")

    mars_dict['facts_table'] = str(soup.find("table", class_="tablepress-id-mars"))

    geo_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(geo_url)
    html = browser.html
    soup = bs(html, "html.parser")

    hemisphere_links = []
    for div in soup.find_all("div", class_="item"):
        link = div.find("a", class_="itemLink product-item")
        hemisphere_links.append(link['href'])

    hemisphere_img_urls = []
    for link in hemisphere_links:
        link_url = "https://astrogeology.usgs.gov" + link
        browser.visit(link_url)
        html = browser.html
        soup = bs(html, "html.parser")
        img_title = soup.find("h2", class_="title").get_text()
        img_dict = {}
        img_dict['title'] = str(img_title)[:-9]
        img_dict['img_url'] = soup.find("a", target="_blank").get('href')
        hemisphere_img_urls.append(img_dict)

    mars_dict['hemisphere_imgs'] = hemisphere_img_urls
    
    return mars_dict


#This is to have data initially stored in MongoDB to pull from 
#for the first use of app.py
import pymongo

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

db = client.mars_db
mars_dict = scrape()
db.mars.drop()
db.mars.insert_one(mars_dict)





