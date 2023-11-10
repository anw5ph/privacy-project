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
    cookies = driver.get_cookies()

    i = 0
    cookie_json = {}
    for cookie in cookies:
        cookie_json[i] = cookie
        i += 1

    return {"result": "Analysis Completed!", "cookies": cookie_json}

if __name__ == '__main__':
    app.run(debug = True)