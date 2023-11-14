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
import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api', methods=['POST'])
def get_cookies():
    data = request.get_json()
    url = data.get('url')

    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920, 1200")
    driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=options)

    driver.get(url)

    # integration_elements = driver.find_elements_by_xpath('//script | //link | //iframe')
    # for element in integration_elements:
    #     try:
    #         tag_name = element.tag_name
    #         outer_html = element.get_attribute("outerHTML")

    #         if tag_name == "script":
    #             src = element.get_attribute("src")
    #             if src and "target" not in src and (("doubleclick" in src) or ("doubleverify" in src) or ("googlesyndication" in src) or ("adservice" in src) or ("adnxs" in src) or ("adroll" in src) or ("adzerk" in src) or ("adform" in src) or ("advertising" in src) or ("adtech" in src) or ("advertising" in src)):
    #                 print("External Script Source:", src)
    #                 print("Element Attributes: ", outer_html)

    #         elif tag_name == "link":
    #             href = element.get_attribute("href")
    #             if href and "target" not in href and (("doubleclick" in href) or ("doubleverify" in href) or ("googlesyndication" in href) or ("adservice" in href) or ("adnxs" in href) or ("adroll" in href) or ("adzerk" in href) or ("adform" in href) or ("advertising" in href) or ("adtech" in href) or ("advertising" in href)):
    #                 print("External Link Href:", href)
    #                 print("Element Attributes: ", outer_html)

    #         elif tag_name == "iframe":
    #             src = element.get_attribute("src")
    #             if src and "target" not in src and (("doubleclick" in src) or ("doubleverify" in src) or ("googlesyndication" in src) or ("adservice" in src) or ("adnxs" in src) or ("adroll" in src) or ("adzerk" in src) or ("adform" in src) or ("advertising" in src) or ("adtech" in src) or ("advertising" in src)):
    #                 print("External Iframe Source:", src)
    #                 print("Element Attributes: ", outer_html)
    #     except StaleElementReferenceException:
    #         print("StaleElementReferenceException - Element no longer exists in the DOM")

    cookies = driver.get_cookies()
    driver.quit()
    i = 0
    cookie_json = {}
    for cookie in cookies:
        cookie_json[i] = cookie
        i += 1

    return {"result": "Analysis Completed!", "cookies": cookie_json}

if __name__ == '__main__':
    app.run(debug = True)