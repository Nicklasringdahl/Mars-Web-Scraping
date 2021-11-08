# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)


def scrape_all():
    browser = init_browser()
    # creating a dictionary for inserting into mongo. 
    mars_scrape = {} 


    # Starting the scraping for mars news.   
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    html = browser.html
    # Parse HTML with Beautiful Soup
    new_soup = BeautifulSoup(html, 'html.parser')
    #Finding the title and paragraphs and adding to variables.
    try:
        slide_elem =  new_soup.select_one('div.list_text')
        first_title = slide_elem.find("div", class_="content_title").get_text()
        first_para = slide_elem.find("div", class_="article_teaser_body").get_text()

    except:
        return None

    
    #Scraping for the featured image.     
    url_img="https://spaceimages-mars.com/"
    browser.visit(url_img) 
    # HTML object
    html_img = browser.html
    # Parse HTML with Beautiful Soup
    soup_img = BeautifulSoup(html_img, 'html.parser')
    #Scraping the image. 
    featured_image=soup_img.find('img', class_="headerimage fade-in")
    featured_image_url=url_img+featured_image['src']


    # Scraping for the Mars Facts. 

    url_facts="https://galaxyfacts-mars.com/"
    tables=pd.read_html(url_facts)

    df=tables[0]
    #Naming the columns
    df.columns=['Description','Mars','Earth']
    #setting the index
    df.set_index('Description',inplace=True)    
    #Convert the scraped data to HTML.
    facts_html=df.to_html()

    # Scraping for the Mars Hemisphere images
    base_url='https://marshemispheres.com/'
    browser.visit(base_url)  
    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup_base = BeautifulSoup(html, 'html.parser')
    #return all results
    hemisphere_scrape=soup_base.find_all('div',class_='item')
    # create an empty list
    hemisphere_images=[]

    # Scraping the image from each url.
    for scrape in hemisphere_scrape: 
        url_hemisphere=base_url+scrape.a['href']
        browser.visit(url_hemisphere)
    
    # Scraping with Beautiful soup.
        html_hemi=browser.html
        soup_hemisphere=BeautifulSoup(html_hemi, 'html.parser')
    
    #scraping the titles
        titles=soup_hemisphere.find('h2', class_ = 'title').text
    
    # finding the full res image. 
        full_res = soup_hemisphere.find('div', class_ = 'downloads')
        image = full_res.find('a')['href']

    #concatinate url 
        image_url=base_url+image
    
    # storing the data in a dictionary 
        hemisphere_images.append({"title": titles, "img_url": image_url})
    
    # returning the data to mongodb 
    mars_scrape= {
        "news_title": first_title,
        "news_paragraph": first_para,
        "featured_image": featured_image_url,
        "facts": facts_html,
        "hemispheres": hemisphere_images
    }
    # Close the browser after scraping
    browser.quit()

    print(mars_scrape)
    print(hemisphere_images)

    return mars_scrape
