import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
from tqdm import tqdm


def browser_startup_sequence():
    # start browser
    base_url = "https://www.google.com/maps/"
    path = r'Google_Maps_Scraper/chromedriver'
    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
    options.add_argument("--lang=en_US")
    driver = webdriver.Chrome(path, chrome_options=options)
    driver.maximize_window()
    driver.set_page_load_timeout(30)
    return driver


def scroll_to_bottom_of_page(webdriver):
    webdriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    return print("Scrolled to bottom of the page")

def close_cookie_window(webdriver):
    # Cookies
    for i in range(10):
        try:
            webdriver.find_element(By.XPATH, '//button[text()="Okay"]').click()
            break
        except:
            time.sleep(2)
            print("No Cookie window available")

def scraper_startup(url):
    driver = browser_startup_sequence()
    driver.get(url)
    time.sleep(5)
    close_cookie_window(driver)
    print("AirBnB Website incl. link successfully loaded and ready to be scraped")
    return driver


def close_translation_window(webdriver):
    check = True
    while check:
        try:
            webdriver.find_element(By.CSS_SELECTOR, 'button[aria-label="Schließen"]').click()
        except:
            time.sleep(2)
            print("No Translation window available")
            check = False

########################################################################
INPUT_URL = 'https://www.airbnb.de/s/London/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&price_filter_input_type=0&price_filter_num_nights=28&query=London%2C%20Vereinigtes%20K%C3%B6nigreich&date_picker_type=flexible_dates&flexible_trip_lengths%5B%5D=one_month&adults=2&source=structured_search_input_header&search_type=autocomplete_click&room_types%5B%5D=Entire%20home%2Fapt&place_id=ChIJdd4hrwug2EcRmSrV3Vo6llI'
INPUT_DESTINATION = "London"
########################################################################

driver = scraper_startup(INPUT_URL)
listings_name_lst, listings_url_lst = ([] for i in range(2))
for i in range(15):
    # Scroll to bottom of page
    time.sleep(5)
    scroll_to_bottom_of_page(driver)
    time.sleep(3)
    # Scrape listings
    soup = BeautifulSoup(driver.page_source, "html.parser")
    listings = soup.find_all("div", {"itemprop": "itemListElement"})
    for listing in listings:
        try:
            name = listing.find("meta", {"itemprop": "name"})["content"]
            listings_name_lst.append(name)
            listing_url = "https://" + listing.find("meta", {"itemprop": "url"})["content"]
            listings_url_lst.append(listing_url)
        except:
            print("Extracting base information failed due to wrong selector")
        print(f"Summary: {name} has Url {listing_url}")
    # Click on next page
    try:
        driver.find_element(By.CSS_SELECTOR, 'a[aria-label="Weiter"]').click()
    except:
        print("No more next button available")
#quit driver
driver.quit()

#extract all information for each listing
i = 0
ratings_lst, ratings_count_lst, price_lst, description_lst = ([] for i in range(4))
driver = scraper_startup(INPUT_URL)
for url in tqdm(listings_url_lst):
    try:
        name = listings_name_lst[i]
        driver.get(url)
        time.sleep(2)
        close_translation_window(driver)
        scroll_to_bottom_of_page(driver)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        try:
            rating = soup.find("span", {"class": "_17p6nbba"}).text.replace(" ·","")
            rating_count = soup.find("span", {"class": "_s65ijh7"}).text.replace(" Bewertungen","")
        except:
            rating = None
            rating_count = None
        try:
            price = soup.find("div", {"class": "_1emnh212"}).find("span", {"class": "_1k4xcdh"}).text.replace("\xa0€","").replace(".","")
        except:
            price = None
        description = soup.find("div", {"data-section-id": "DESCRIPTION_DEFAULT"}).text
        ratings_lst.append(rating)
        ratings_count_lst.append(rating_count)
        price_lst.append(price)
        description_lst.append(description)
        print(f"### Name: {name} | Rating: {rating} with {rating_count} Ratings | Price: {price} ###")
        i += 1
        time.sleep(random.randint(1, 3))
    except:
        rating = None
        rating_count = None
        price = None
        description = None
        ratings_lst.append(rating)
        ratings_count_lst.append(rating_count)
        price_lst.append(price)
        description_lst.append(description)

driver.quit()
print("Scraping done")
listing_df = pd.DataFrame({'Listing':listings_name_lst, 'Price': price_lst, 'Rating':ratings_lst, 'Review Count':ratings_count_lst, 'URL':listings_url_lst, 'Description':description_lst})
listing_df.to_excel(f"AirBnB_{INPUT_DESTINATION}.xlsx")
