from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver

import threading
import random
import json
import math
import os

print("\033c")
print("padlet-spammer v1.2 by @p55d2k and @InsanelyAvner")
print("NOTE: DO NOT LEAVE THE CHROME WINDOW WHILE THE SCRIPT IS RUNNING\n")
    
with open("config.json") as f:
    config = json.load(f)

if not "link" in config or not "comments" in config or not "like" in config:
    raise Exception("Invalid config file")

if "amt" in config:
    if type(config["amt"]) != int:
        raise Exception("Invalid config file")
    amount = config["amt"]
else:
    amount = math.inf
    
if "threads" in config:
    if type(config["threads"]) != int:
        raise Exception("Invalid config file")
    THREADS = config["threads"]
else:
    THREADS = 2
    
showwindow = True

url = config["link"]
comment_type = config["comments"]
like = config["like"]

if type(like) != bool or type(comment_type) != str or type(url) != str:
    raise Exception("Invalid config file")

if comment_type not in ["positive", "negative", "none"]:
    raise Exception("Invalid comment type")

if not os.path.exists("comments"):
    raise Exception("comments folder not found")

if not os.path.exists("comments/positive.json") or not os.path.exists("comments/negative.json"):
    raise Exception("comments/positive.json or comments/negative.json not found")

if comment_type == "positive":
    with open("comments/positive.json") as f:
        comments = json.load(f)
elif comment_type == "negative":
    with open("comments/negative.json") as f:
        comments = json.load(f)

chrome_options = Options()
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
if not showwindow:
    chrome_options.add_argument("--headless")

count = 1

def worker():
    global count, amount

    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()

    while amount > 0:
        print(f"\nIteration {count} on thread {threading.current_thread().name}")
        driver.get(url)

        wait = WebDriverWait(driver, 10)

        if like:
            like_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="surface-container"]/div[4]/div[2]/div/div[2]/div/div[3]/button')))
            like_button.click()
        
        if comment_type == "none":
            count += 1
            amount -= 1
            driver.delete_all_cookies()
            continue
        
        comment_box = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="surface-container"]/div[4]/div[2]/div/div[2]/div/div[4]/div[2]/div/div/div/div/div/p')))
        comment_box.send_keys(random.choice(comments))
        
        comment_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="surface-container"]/div[4]/div[2]/div/div[2]/div/div[4]/div[2]/div/button')))
        comment_button.click()

        amount -= 1
        count += 1
        driver.delete_all_cookies()
        
threads = []

for i in range(THREADS):
    thread = threading.Thread(target=worker)
    thread.start()
    threads.append(thread)
    
for thread in threads:
    thread.join()
    
print("\nDone!")