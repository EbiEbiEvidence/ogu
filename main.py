import sys
import os
from pathlib import Path
from time import sleep
from dotenv import load_dotenv
from selenium.common.exceptions import NoAlertPresentException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def main():
    # Load .env
    dotenv_path = Path(".env")
    load_dotenv(str(dotenv_path))
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")

    # Init driver
    driver_options = Options()
    driver_options.add_argument("--headless")
    driver = webdriver.Chrome(options=driver_options)

    # Get login page
    driver.get("https://www.e-license.jp/el/ogu/")

    # Wait for the redirection is completed
    sleep(1)

    driver.find_element_by_id("p01aForm_b_studentId").send_keys(username)
    driver.find_element_by_id("p01aForm_b_password").send_keys(password)
    driver.find_element_by_id("p01aForm_login").click()

    # Wait for the login is succeeded
    sleep(1)

    # If you are failed to login, an alert will be shown.
    try:
        driver.switch_to.alert.accept()
        sys.stderr.write("Username or password is invalid\r\n")
        exit()

    # If there are no alert, `NoAlertPresentException` will be raised.
    except NoAlertPresentException as _:
        pass

    # Save it
    driver.save_screenshot("success.png")


if __name__ == "__main__":
    main()
