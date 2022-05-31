#import dependencies
from bs4 import BeautifulSoup as be_so
import requests
import pymongo
from splinter import Browser
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape():
    exec_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **exec_path, headless=False)


    url = 'https://redplanetscience.com/'
    browser.visit(url)
    time.sleep(5)

    ## get the page scraped and into beautiful Soup

    html_ = browser.html
    sp = be_so(html_, "html.parser")

    #find the titles and parragraphs

    titles = sp.find_all('div',class_="content_title")[0].text
    parragraph = sp.find_all('div',class_="article_teaser_body")[0].text


    # Get images! to get them define url to collect from

    marsimages_url = 'https://spaceimages-mars.com/'
    browser.visit(marsimages_url)   
    time.sleep(5)

    ##browse the url, scrape the data into beautiful soup

    html_=browser.html
    soup=be_so(html_, 'html.parser')
    imgs_url = soup.find("a", class_ = "showimg fancybox-thumbs")["href"]
    featured_img_url = marsimages_url + imgs_url


    # Collect fact table about mars - set url

    fact_url = "https://galaxyfacts-mars.com"
    browser.visit(fact_url)

    ## gather the table and store in a dataframe 

    tables_ = pd.read_html(fact_url)
    data_df = tables_[1]
    data_df.columns = ["description", "value"]
    data_df.set_index("description", inplace=True)
    html_dataframe = data_df.to_html()

    ##hemispheres data colletions, start with url
    hemis_url = "https://marshemispheres.com/"
    browser.visit(hemis_url)

    #Perform scrapping and add into beutiful soup
    time.sleep(4)
    hemis_html = browser.html
    soup = be_so(hemis_html, 'html.parser')
    items = soup.find_all("div", class_="item")
    hem_urls = []

    #Create a loop to collect data from all (4) hemispheres

    for i in range(4):
    #create empty dictionary
        hemispheres = {}
        browser.find_by_css('a.product-item h3')[i].click()
        element = browser.links.find_by_text('Sample').first
        img2_url = element['href']
        title = browser.find_by_css("h2.title").text
        hemispheres["img_url"] = img2_url
        hemispheres["title"] = title
        hem_urls.append(hemispheres)
        browser.back()

    mars_data = {
            "news_title": titles,
            "news_paragraph": parragraph,
            "facts": html_dataframe,
            "featured_image": featured_img_url,
            "hemispheres": hem_urls
    }

    # In[16]:


    browser.quit()
    return mars_data

