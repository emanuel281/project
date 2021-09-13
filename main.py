import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def main():

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(executable_path='./bin/chromedriver',
                              options=chrome_options)
    driver.implicitly_wait(7)

    URL = 'https://www.twitter.com/login'
    driver.get(URL)
    assert "Twitter" in driver.title

    with open('./logins.txt', 'r') as f:
        user = f.readline()
        passw = f.readline()

        assert user and passw

        login(user, passw, dr=driver)

        try:
            like_post(driver)
        finally:
            time.sleep(30)
            driver.close()


def login(user, passw, dr=None):
    if dr is not None:
        form = dr.find_element_by_tag_name('form')
        username = form.find_element_by_xpath(
            "//input[@name='session[username_or_email]']")
        username.send_keys(f'{user}')
        password = form.find_element_by_xpath(
            "//input[@name='session[password]']")
        password.send_keys(f'{passw}', Keys.RETURN)
        print("Logged in...")


def like_post(dr=None):
    if dr is not None:
        article0 = WebDriverWait(dr, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, 'article'))
        )
        print(article0.text)
        like = article0.find_element_by_xpath("//div[@data-testid='like']")
        like.click()
        print("Liked the post...")


if __name__ == '__main__':
    main()

