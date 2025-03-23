import time
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
import time
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import os
def scroll_followers():
    # Find the scrollable div within the pop-up
    popup = driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]')

    # Scroll within the scrollable div
    last_height = driver.execute_script("return arguments[0].scrollHeight", popup)

    while True:
        # Scroll to the bottom of the div
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", popup)
        
        # Wait for content to load
        time.sleep(2)
        
        # Get the new height after scrolling
        new_height = driver.execute_script("return arguments[0].scrollHeight", popup)
        
        # Break the loop if the height doesn't change (meaning we've reached the bottom)
        if new_height == last_height:
            break
        
        last_height = new_height

    print("Reached the bottom of the pop-up!")
def click_followers():
    xpath = '/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/header/section[3]/ul/li[3]/div/a/span'

    # Wait until the element is clickable
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    )

    # Click the element
    element.click()
    
def get_followers():
    source = driver.page_source
    soup = BeautifulSoup(source, "html.parser")
    div = soup.find(class_='xyi19xy x1ccrb07 xtf3nb5 x1pc53ja x1lliihq x1iyjqo2 xs83m0k xz65tgg x1rife3k x1n2onr6')
    r_accounts = div.find_all(class_='x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1n2onr6 x1plvlek xryxfnj x1c4vz4f x2lah0s x1q0g3np xqjyukv x6s0dn4 x1oa3qoh x1nhvcw1')
    with open('Raccounts.txt', 'a') as file:
        for r in r_accounts:
            r_account = r.text
            file.write(r_account)
            file.write('\n')



def get_posts():
    source = driver.page_source
    soup = BeautifulSoup(source, "html.parser")
    posts_div = soup.find(class_='xg7h5cd x1n2onr6')
    if posts_div:
        posts_divs = posts_div.find_all(class_='x1lliihq x1n2onr6 xh8yej3 x4gyw5p x11i5rnm x1ntc13c x9i3mqj x2pgyrj')
        posts = []
        for post_div in posts_divs:
            post = post_div.find('a')['href']
            posts.append(post)
        return posts
    else:
        return None
def get_last_post(file_path):
    # Check if the file exists
    if os.path.exists(file_path):
        # If the file exists, open it and load the data
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
        
        # Get the list of all posts
        all_posts = data.get('all_posts', [])
        
        # Check if there are any posts
        if all_posts:
            # Get the last post (the last element in the list)
            last_post = all_posts[0]
            print(f"The last post is: {last_post}")
        else:
            print("No posts found in the file.")
        return last_post
    else:
        print(f"The file {file_path} does not exist.")
        return None
def scroll_account(last_post):
    # Get the initial page height
    last_height = driver.execute_script("return document.body.scrollHeight")
    post_found = False

    # Scroll until reaching the end
    while True:
        # Wait for the loading icon to disappear (invisible)
        try:
            # Wait until the loading icon is not visible
            WebDriverWait(driver, 10).until(
                EC.invisibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/div[2]/div[2]/div/svg/rect[12]'))
            )
        except:
            print("Timed out waiting for the loading icon to disappear.")

        # Scroll down to the bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Wait for new content to load (adjust the time if necessary)
        time.sleep(3)
        
        # Get the new page height
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        # Break the loop if the page height doesn't change (reached the bottom)
        if new_height == last_height:
            break
        
        if last_post:
            source = driver.page_source
            soup = BeautifulSoup(source, "html.parser")
            posts_div = soup.find(class_='xg7h5cd x1n2onr6')
            if posts_div:
                posts_divs = posts_div.find_all(class_='x1lliihq x1n2onr6 xh8yej3 x4gyw5p x11i5rnm x1ntc13c x9i3mqj x2pgyrj')
                for post_div in posts_divs:
                    post = post_div.find('a')['href']
                    if post == last_post:
                        post_found = True
                        break
            if post_found:
                break

        # Update the last height for the next iteration
        last_height = new_height
# Path to your Chrome user data directory
#profile = r"C:\Users\black\AppData\Local\Google\Chrome\User Data\Profile 9"  # Change this path
profile = r"C:\Users\black\AppData\Local\Google\Chrome\User Data\instagram"  # Change this path

# Set up Chrome options
options = Options()
options.add_argument(f"user-data-dir={profile}")  # Path to user data
global driver 
# Initialize undetected-chromedriver with the custom profile
driver = uc.Chrome(options=options, use_subprocess=True)
# Use Chrome DevTools to block images and videos
driver.execute_cdp_cmd("Network.setBlockedURLs", {"urls": ["*.jpg", "*.png", "*.gif", "*.mp4", "*.webm", "*.avi"]})
driver.execute_cdp_cmd("Network.enable", {})
# Open Instagram in the same tab
driver.get("https://instagram.com")
time.sleep(6)  # Wait for the page to load

# Quit the driver
with open('Raccounts.txt', 'r') as file:
    accounts = [line.strip() for line in file.readlines()]
deleted_accounts = []



for account in accounts:
    driver.get(f'https://www.instagram.com/{account}')
    last_post = get_last_post(f'{account}.json')
    time.sleep(5)
        
    scroll_account(last_post)
    posts = get_posts()
    if posts:
        pictures = []
        reels = []
        
        for post in posts:
            if post.split("/")[2] == 'p':
                pictures.append(post)
            else:
                reels.append(post)
        # Create a dictionary to store the data
        data = {
            "account": account,
            "all_posts": posts,  # Add all posts to the dictionary
            "pictures": pictures,
            "reels": reels
        }

        # Path to store the JSON file
        file_path = f"{account}.json"

        # Function to remove duplicates from a list while preserving the order
        def remove_duplicates(posts_list):
            return list(dict.fromkeys(posts_list))

        # Check if the file already exists
        if not os.path.exists(file_path):
            # If the file doesn't exist, create it and write the data
            with open(file_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)
        else:
            # If the file exists, load the existing data, add new data, and update the file
            with open(file_path, 'r') as json_file:
                existing_data = json.load(json_file)
            
            # If the account already exists in the file, append data to it
            if existing_data.get("account") == account:
                # Remove duplicates from the lists before extending
                existing_data["all_posts"] = remove_duplicates(posts + existing_data["all_posts"])  # Add new posts at the top
                existing_data["pictures"] = remove_duplicates(pictures + existing_data["pictures"])  # Add new pictures at the top
                existing_data["reels"] = remove_duplicates(reels + existing_data["reels"])  # Add new reels at the top
            
            # Save the updated data back to the JSON file
            with open(file_path, 'w') as json_file:
                json.dump(existing_data, json_file, indent=4)
    else:
        deleted_accounts.append(account) 

        
driver.quit()