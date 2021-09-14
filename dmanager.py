from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
import pygsheets
import winsound
from typing import List, Dict, Tuple
import sys
import time

from dndbeyond_crawler import scrape, upload, create_update_records, update_on_site
from defaults import *


class DManager:
    """"""
    def __init__(self, characters: Dict[str, str] = None, purpose: str = None):
        self._characters = CHARACTERS if not characters else characters
        self._purpose = purpose
        self._connection_browser, self._is_loaded = self.establish_connection()
        self._google_connection = pygsheets.authorize(client_secret='token.json')
        if not self._purpose:
            self.get_purpose()

    def get_purpose(self):
        purpose = input("Beep, What is my purpose? \n(1: update sheet, 2: update sheet & items, 3: update items)\n")
        while purpose not in ["1", "2", "3"]:
            print("That's not even a purpose, what kind of human overlord are you? beep boop")
            purpose = input("Bep, What is my purpose? \n(1: update sheet, 2: update sheet & items, 3: update items)\n")
        print(f"Oh god, I {'update sheet' if purpose == '1' else 'update items' if purpose == '3' else 'update sheet & items'}")
        self._purpose = purpose

    def run(self) -> None:
        if self._purpose in ['1', '2']:
            print("I'll begin crawling, since that's always my purpose, bippi boopi")
            try:
                self.crawl()
            except Exception as e:
                print("Since I encountered an issue while crawling, I will shut down now and let you handle it. "
                      "Please be gentle with me, I really tried")
                sys.exit(e)
        if self._purpose == '1':
            print("That's all you asked from me, goodbyoop")
            sys.exit(0)
        try:
            self.update_beyond()
        except Exception as e:
            print("Since I encountered an issue while updating, I will shut down now and let you handle it. "
                  "Please be gentle with me, I really tried")
            sys.exit(e)

    def establish_connection(self) -> Tuple[Chrome, str]:
        print("Establishing browser connection, beep boop bop bip I'm a bot")
        browser = webdriver.Chrome(executable_path=DRIVER_PATH)
        browser.implicitly_wait(10)
        browser.get(self._characters["Viv"])
        # TODO - make more general
        body = WebDriverWait(browser, timeout=60).until(lambda d: d.find_element_by_tag_name("body"))
        is_loaded = body.text
        return browser, is_loaded

    def verify_humanity(self, browser):
        # title Access to this page has been denied.
        # <div id="NVqimXqYVTwgIxE" class="taSkWkCrMMVNJeG"><div id="vEemahLMTWaoLMe"></div><div id="jqSAGtBuAMuDafn" role="main" aria-label="Human Challenge requires verification. Please press and hold the button until verified"><div id="XXyEtzbRmHQWNEy"></div><p id="VWqUAZwzVrQtBNN" class="GoMXBWLaKOqhiDr">Press &amp; Hold</p><div class="fetching-volume"><span>•</span><span>•</span><span>•</span></div><div id="checkmark"></div><div id="ripple"></div></div></div>
        pass


    def crawl(self):
        try:
            equipment_all = {}
            actual_items = {}
            actual_items, can_carry = scrape(self._connection_browser, self._is_loaded, equipment_all, actual_items)
            print("Finished getting data for all characters. Now starting sheet upload, bippi di boop doop")
            characters = Chars({cha: [item.split('\n', maxsplit=5) for item in items
                                if '\n' in item and 7 > item.count('\n') > 1 and item[0] != '+']
                                for cha, items in actual_items.items()})
            upload(characters, can_carry, self._google_connection)
            print("Finished uploading, are you proud of me?")
            duration = 1000  # milliseconds
            freq = 440  # Hz
            winsound.Beep(freq, duration)
        except Exception as e:
            raise e

    def update_beyond(self):
        try:
            print("Bipp, creating records for updating stuff")
            records = create_update_records(self._google_connection)
            print("Created records, your..... highness, now log to the site to enable me to edit")
            self.login_to_beyond(self._connection_browser)
            print("Great, let's move on")
            update_on_site(self._connection_browser, records)
            print("Finished updating, am I a good bot?")
        except Exception as e:
            raise e

    @staticmethod
    def login_to_beyond(browser: Chrome):
        username = input("Please give me your username, promise I won't do anything bad with it ;)\n")
        password = input("Please give me your password, it won't be used for world domination usually\n")
        print("Currently Supports Only Twitch Login")
        login = browser.find_element_by_css_selector(LOGIN)
        login.click()
        twitch = browser.find_element_by_css_selector('button[id="signin-with-twitch"]')
        twitch.click()
        browser.find_element_by_css_selector(USERNAME).send_keys(username)
        browser.find_element_by_css_selector(PASSWORD).send_keys(password)
        click_to_login = browser.find_element_by_css_selector('div[class="Layout-sc-nxg1ff-0 ivVfMD"]')
        click_to_login.click()
        print("Now I need you to enter your validation code and authorize me")
        duration = 2000  # milliseconds
        freq = 840  # Hz
        winsound.Beep(freq, duration)
        time.sleep(30)


if __name__ == '__main__':
    runner = DManager(CHARACTERS)
    runner.run()
