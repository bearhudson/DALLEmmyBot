import webbrowser
import os

from httpcore import TimeoutException
from imgur_python import Imgur
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

CLIENT_ID = os.getenv("IMGUR_ID")
CLIENT_SECRET = os.getenv("IMGUR_SECRET")

imgur_client = Imgur({'client_id': f'{CLIENT_ID}', 'client_secret': f'{CLIENT_SECRET}'})
auth_url = imgur_client.authorize()
web_driver = webdriver.Chrome()
web_driver.get(f"{auth_url}")
web_driver.implicitly_wait(2)
username_box = web_driver.find_element(By.NAME, "username")
password_box = web_driver.find_element(By.NAME, "password")
allow_button = web_driver.find_element(By.NAME, "allow")
username_box.send_keys(f"{os.getenv('IMGUR_USER')}")
password_box.send_keys(f"{os.getenv('IMGUR_PASSWORD')}")
web_driver.implicitly_wait(30)
allow_button.click()

redirect_url = "expected_redirect_url"
redirect_timeout = 30  # seconds
try:
    # Wait until the current URL changes to the expected redirect URL
    WebDriverWait(web_driver, redirect_timeout).until(EC.url_to_be(redirect_url))
    # Get the final URL after the redirect
    final_url = web_driver.current_url
    print(f"Redirect successful. Final URL: {final_url}")
except TimeoutException:
    print(f"Timeout waiting for redirect to {redirect_url}")
