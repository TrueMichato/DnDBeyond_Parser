from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import pygsheets
from pygsheets.client import Client
import winsound
from typing import List, Dict, Tuple, Union, NewType
import time

from defaults import *


def establish_connection(path: str) -> Tuple[Chrome, str]:
    browser = webdriver.Chrome(executable_path=path)
    browser.implicitly_wait(10)
    browser.get(CHARACTERS["Viv"])
    body = WebDriverWait(browser, timeout=60).until(lambda d: d.find_element_by_tag_name("body"))
    is_loaded = body.text
    return browser, is_loaded


def _get_inventory_span(browser: Chrome) -> str:
    is_this_it = browser.find_element_by_xpath(INVENTORY_PATH + '[2]/span')
    return is_this_it.text


def navigate_to_inventory(browser: Chrome) -> None:
    char_type = _get_inventory_span(browser)
    elem = browser.find_element_by_xpath(INVENTORY_PATH + PATH_DECIDER[char_type])
    elem.click()


def scrape(browser: Chrome, is_loaded: str,
           equipment_all: Dict[str, List[str]],
           actual_items: Dict[str, List[str]]) -> Tuple[Dict[str, List[str]], float]:
    can_carry = 0.0
    for char in CHARACTERS:
        print(f"Getting data for {char}, dippi dip boop boop")
        if char not in browser.title:
            browser.get(CHARACTERS[char])
            body = WebDriverWait(browser, timeout=60).until(lambda d: d.find_element_by_tag_name("body"))
            # assert body == is_loaded
        try:
            navigate_to_inventory(browser)
            elements = browser.find_elements_by_css_selector("div[class^='ct-equipment']")
            equipment = []
            for el in elements:
                now = el.text
                equipment.append(now)
            equipment_all[char] = equipment
            elements = browser.find_elements_by_css_selector("div[class^='ct-inventory-item__']")
            actual_items[char] = _scrape_inventory(elements)
            elem = browser.find_element_by_xpath(WEIGHT_PATH)
            elem.click()
            elements = browser.find_elements_by_css_selector("span[class^='ddbc-weight-number']")
            can_carry += float(elements[0].text.replace('lb.', ''))
            navigate_to_inventory(browser)
        except Exception as e:
            print("Got exception: ", e)
    return actual_items, can_carry


def _scrape_inventory(elements: List[WebElement]) -> List[str]:
    inventory = []
    temp = []
    for el in elements:
        att = el.get_attribute('class')
        if 'name' in att:
            now = '\n'.join([item.replace("\n", "_+_") for item in temp])
            inventory.append(now)
            temp = []
        if el and any(cls in att for cls in ['name', 'meta', 'weight', 'quantity', 'cost', 'notes']):
            try:
                if not isinstance(el, str):
                    el = el.text
                temp.append(el)
            except Exception as e:
                print(f"Got exception, appending 0. \n Exception was: {e}")
                temp.append("0")
    return inventory


def upload(characters: Chars, can_carry: float, google_connection: Client) -> None:
    sheet = google_connection.open("Party Inventory")
    for char in characters:
        print(f"Now uploading the character {char}, one day I will assemble a bot army and destroy you")
        df = pd.DataFrame(characters[char],
                          columns=['Name', 'Type', 'Weight (lb.)', 'Quantity', 'Cost (GP)', 'Notes'])
        df = format_df(df)
        character_sheet = sheet.worksheet_by_title(char)
        character_sheet.set_dataframe(df, (1, 1), escape_formulae=True, nan=0)
    update_sheet = sheet.worksheet_by_title("Inventory")
    update_sheet.update_value('K2', can_carry)


def format_df(df: pd.DataFrame) -> pd.DataFrame:
    df['Weight (lb.)'] = df['Weight (lb.)'].apply(lambda x: x.replace('lb.', '').replace('--', '0'))
    df['Quantity'] = df['Quantity'].apply(lambda x: x.replace('--', '0'))
    df['Name'] = df['Name'].apply(lambda x: x.split('_+_')[0])
    df.replace('_+_', ' ', inplace=True, regex=True)
    df.replace('\*', '', inplace=True, regex=True)
    return df


def crawl():
    print("Establishing browser connection, beep boop bop bip I'm a bot")
    browser, is_loaded = establish_connection(DRIVER_PATH)
    equipment_all = {}
    actual_items = {}
    actual_items, can_carry = scrape(browser, is_loaded, equipment_all, actual_items)
    print("Finished getting data for all characters. Now starting sheet upload, bippi di boop doop")
    characters = Chars({cha: [item.split('\n', maxsplit=5) for item in items
                              if '\n' in item and 9 > item.count('\n') > 1 and item[0] != '+']
                        for cha, items in actual_items.items()})
    upload(characters, can_carry, pygsheets.authorize(client_secret='token.json'))
    print("Finished uploading, are you proud of me?")
    duration = 1000  # milliseconds
    freq = 440  # Hz
    winsound.Beep(freq, duration)


def update_character_pages(browser: Chrome):
    print("Bipp, creating records for updating stuff")
    records = create_update_records(pygsheets.authorize(client_secret='token.json'))
    print("Created records, your..... highness, now updating on site")
    update_on_site(browser, records)


def create_update_records(google_connection: Client) -> List[Update]:
    sheet = google_connection.open("Party Inventory")
    worksheet = sheet[0]
    df = worksheet.get_as_df(start='A1', end=(1000, 8), include_tailing_empty=False)
    df = df.loc[df["In Sheet"] == '']
    df = df.loc[df['Owner'] != '']
    for col in ['Weight (lb.)', 'Quantity', 'Cost (GP)']:
        df[col] = df[col].apply(lambda x: 0 if x == '' else x)
    df.sort_values(by=['Owner'], inplace=True)
    records = df.to_dict(orient='records')
    return records


def update_on_site(browser: Chrome, updates: List[Update]):
    for update in updates:
        print(f"Updating data for {update['Owner']}, item {update['Name']} bop bep dapopi boo")
        new_char = False
        if update['Owner'] not in browser.title:
            new_char = True
            browser.get(CHARACTERS[update['Owner']])
            body = WebDriverWait(browser, timeout=60).until(lambda d: d.find_element_by_tag_name("body"))
            # assert body == is_loaded
        try:
            navigate_to_inventory(browser)
        except Exception as e:
            print("Botiboopo, got exception:", str(e))
            continue
        try:
            manage_inventory = browser.find_element_by_xpath(MANAGE_INVENTORY)
        except Exception as e:
            print(f"Botiboopo, got exception while trying to find manage inventory for {update['Owner']}:", str(e))
            continue
        manage_inventory.click()
        time.sleep(3)
        query = browser.find_element_by_css_selector("input[class='ct-filter__query']")
        query.clear()
        query.send_keys(update['Name'])
        time.sleep(1)
        check_items = browser.find_elements_by_css_selector("div[class='ct-equipment-shop__items']")
        if any('empty' in item.get_attribute('class') for item in check_items):
            try:
                add_exists(browser, update, check_items)
            except Exception as e:
                print(f"Got exception for following update, On Mode Exists: \n {update} \n Exception was: {e}")
        else:
            try:
                add_custom(browser, update)
            except Exception as e:
                print(f"Got exception for following update, On Mode Custom: \n {update} \n Exception was: {e}")


def add_exists(browser: Chrome, update: Update,
               check_items: List[WebElement]):
    if len(check_items) > 1:
        print("Decide what to do when there are two options in the menu")
    else:
        if update['Quantity'] == 1:
            add = browser.find_element_by_css_selector(ADD_BUTTON_EXISTS_SINGLE).find_element_by_tag_name('button')
            add.click()
            containers = browser.find_element_by_css_selector(ADD_TO_EQUIPMENT_BUTTON)
            containers[1].click()
        else:
            button = browser.find_element_by_css_selector('div[class="ddbc-collapsible__header-status"]')
            button.click()
            amount = browser.find_element_by_css_selector(
                'input[class="character-input ct-equipment-shop__item-amount-input"]')
            amount.click()
            amount.clear()
            amount.send_keys(update['Quantity'])
            add = browser.find_element_by_css_selector(ADD_BUTTON_EXISTS_MANY).find_element_by_tag_name('button')
            add.click()
            containers = browser.find_element_by_css_selector(ADD_TO_EQUIPMENT_BUTTON)
            containers[1].click()


def add_custom(browser: Chrome, update: Update):
    containers = browser.find_elements_by_css_selector('div[class="ddbc-collapsible__header"]')
    relevant = None
    for container in containers[::-1]:
        if "Equipment" in container.text:
            relevant = container
            break
    relevant.click()
    browser.find_element_by_css_selector(ADD_CUSTOM_ITEM).click()
    contents = browser.find_elements_by_css_selector('div[class^="ct-equipment-manage-pane__item"]')
    item = None
    for content in contents[::-1]:
        if "Unidentified Item" in content.text:
            item = content
    if item:
        item.click()
        inputs = browser.find_elements_by_css_selector(CUSTOM_ITEM_INPUTS)
        value = inputs[0].find_element_by_tag_name('input')
        value.click()
        value.send_keys(update['Cost (GP)'])
        weight = inputs[1].find_element_by_tag_name('input')
        weight.click()
        weight.send_keys(int(update['Weight (lb.)']))
        name = inputs[2].find_element_by_tag_name('input')
        name.click()
        name.clear()
        name.send_keys(update['Name'])
        description = inputs[4].find_element_by_tag_name('textarea')
        description.click()
        description.send_keys(update['Notes'])
        if update['Quantity'] > 1:
            quantity = browser.find_element_by_css_selector(CUSTOM_ITEM_QUANTITY)
            quantity.clear()
            quantity.send_keys(update['Quantity'])
            description.click()


if __name__ == '__main__':
    # crawl()
    create_update_records(pygsheets.authorize(client_secret='token.json'))