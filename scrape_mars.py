from bs4 import BeautifulSoup
import pandas as pd
from splinter import Browser
import requests
import pymongo

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)  

def scrape():
    browser = init_browser()
    mars_dict = {}


    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'

    # Retrieve page with the requests module
    response = requests.get(url)
    # Create BeautifulSoup object; parse with 'lxml'
    soup = BeautifulSoup(response.text, 'html.parser')

    news_title = soup.find("div",class_="content_title").text
    # mars_dict['news_title'] = news_title

    news_p = soup.find("div", class_="rollover_description_inner").text
    # mars_dict['news_p']= news_p

    # JPL Mars Space Images with splinter

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    html = browser.html
    soup2 = BeautifulSoup(html, 'html.parser')

    image = soup2.find('article', class_='carousel-item')
    featured_image_url = 'https://www.jpl.nasa.gov' + image
    featured_image_url

    #Mars Facts- using Pandas

    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    df = tables[0]
    html_table = df.to_html()
    html_table.replace('\n', '')

    # Mars Hemispheres
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    base_url = 'https://astrogeology.usgs.gov'
    next_page_urls = []
    img_titles = []

    # Get soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    print(soup.prettify())

    divs = soup.find_all('div', class_='description')

    #For loop to pull all hrefs

    counter = 0
    for div in divs:
        link = div.find('a')
        href = link['href']
        img_title = div.a.find('h3')
        img_title = img_title.text
        img_titles.append(img_title)
        next_page = base_url + href
        next_page_urls.append(next_page)
        counter = counter + 1
        if (counter == 4):
            break
            
    # print(next_page_urls)
    # print(img_titles)

    # Loop for next page images

    np_images = []

    for next_page_url in next_page_urls:
        url=next_page_url
        browser.visit(url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        link2 = soup.find('img', class_="wide-image")
        src = link2['src']
        full_img = base_url + src
        np_images.append(full_img)
        
    np_images  

    # Creating the dictionaries

    hemisphere_image_urls = []

    cerebrus = {'title': img_titles[0], 'img_url': np_images[0]}
    schiaparelli = {'title': img_titles[1], 'img_url': np_images[1]}
    syrtis = {'title': img_titles[2], 'img_url': np_images[2]}
    valles = {'title': img_titles[3], 'img_url': np_images[3]}

    hemisphere_image_urls = [cerebrus, schiaparelli, syrtis, valles]
    # print(hemisphere_image_urls)

    #Mars dictionary

    mars_dict = {
        "news_title": news_title,
        "news_p": news_p, 
        "featured_image_url": featured_image_url, 
        "Mars_facts": str(html_table), 
        "hemisphere_images": hemisphere_image_urls
    }

    return mars_dict

if __name__ == "__main__":
    scrape()