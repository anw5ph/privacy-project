# DO NOT RUN THIS FILE IT IS NOT USED ANYMORE IN THE PROJECT
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import time
import pandas as pda
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/firstParty', methods=['POST'])
def get_cookies():
    data = request.get_json()
    url = data.get('url')

    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920, 1200")
    options.add_argument("start-maximized")
    # options.add_argument("--auto-open-devtools-for-tabs")
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    driver.get(url)
    time.sleep(30)

    i = 0
    first_party_cookie_json = {}
    first_party_cookies = driver.get_cookies()
    print(len(first_party_cookies))
    for cookie in first_party_cookies:
        first_party_cookie_json[i] = cookie
        i += 1

    driver.close()

    return {"result": "Analysis Completed!", "first_party_cookies": first_party_cookie_json, "first_party_cookies_length": len(first_party_cookies)}

if __name__ == '__main__':
    app.run(debug = True)

    # script_tags = driver.find_elements_by_tag_name('script')
    # # Analyze script tags for external sources
    # for script_tag in script_tags:
    #     src_attribute = script_tag.get_attribute('src')
    #     if src_attribute:
    #         print()
    #         print(f"External Script Source: {src_attribute}")

    # # Find all iframes
    # iframes = driver.find_elements_by_tag_name('iframe')
    # # Analyze iframes for external sources
    # for iframe in iframes:
    #     src_attribute = iframe.get_attribute('src')
    #     if src_attribute:
    #         print()
    #         print(f"External Iframe Source: {src_attribute}")


# integration_elements = driver.find_elements_by_xpath('//script | //link | //iframe')
    # for element in integration_elements:
    #     try:
    #         tag_name = element.tag_name
    #         # outer_html = element.get_attribute("outerHTML")

    #         if tag_name == "script":
    #             src = element.get_attribute("src")
    #             if src and "target" not in src and (("doubleclick" in src) or ("doubleverify" in src) or ("googlesyndication" in src) or ("adservice" in src) or ("adnxs" in src) or ("adroll" in src) or ("adzerk" in src) or ("adform" in src) or ("advertising" in src) or ("adtech" in src) or ("advertising" in src)):
    #                 print("External Script Source:", src)
    #                 # print("Element Attributes: ", outer_html)
    #                 print()

    #         elif tag_name == "link":
    #             href = element.get_attribute("href")
    #             if href and "target" not in href and (("doubleclick" in href) or ("doubleverify" in href) or ("googlesyndication" in href) or ("adservice" in href) or ("adnxs" in href) or ("adroll" in href) or ("adzerk" in href) or ("adform" in href) or ("advertising" in href) or ("adtech" in href) or ("advertising" in href)):
    #                 print("External Link Href:", href)
    #                 # print("Element Attributes: ", outer_html)
    #                 print()

    #         elif tag_name == "iframe":
    #             src = element.get_attribute("src")
    #             if src and "target" not in src and (("doubleclick" in src) or ("doubleverify" in src) or ("googlesyndication" in src) or ("adservice" in src) or ("adnxs" in src) or ("adroll" in src) or ("adzerk" in src) or ("adform" in src) or ("advertising" in src) or ("adtech" in src) or ("advertising" in src)):
    #                 print("External Iframe Source:", src)
    #                 # print("Element Attributes: ", outer_html)
    #                 print()
    #     except StaleElementReferenceException:
    #         print("StaleElementReferenceException - Element no longer exists in the DOM")
    #     except NoSuchElementException:
    #         print("NoSuchElementException - Element not found in the DOM")