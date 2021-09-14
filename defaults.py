CHARACTERS = {"Viv": "https://www.dndbeyond.com/profile/Smolll/characters/45333304",
              "Moon": "https://www.dndbeyond.com/profile/Tamarooshia/characters/42803442",
              "Lunaria": "https://www.dndbeyond.com/profile/CelinaMeckrox/characters/45382321",
              "Sharx": "https://www.dndbeyond.com/profile/IdoZemach/characters/46625409",
              "Dick": "https://www.dndbeyond.com/profile/Tokag/characters/45331060"}

# CHARACTERS = {"Moon": "https://www.dndbeyond.com/profile/Tamarooshia/characters/42803442"}

DRIVER_PATH = 'C:/Users/user/Documents/Coding/DnDBeyond_Parser/chromedriver'
PATH_DECIDER = {'INVENTORY': '[2]', 'SPELLS': '[3]'}
INVENTORY_PATH = '//*[@id="character-tools-target"]/div/div[2]/div/div/div[3]/div[6]/div/div[2]/div[1]/div'
WEIGHT_PATH = '//*[@id="character-tools-target"]/div/div[2]/div/div/div[3]/div[6]/div/div[2]/div[2]/div/div/div[1]/div/div[1]/div[1]/span[2]/span/span[1]'

MANAGE_INVENTORY = '//*[@id="character-tools-target"]/div/div[2]/div/div/div[3]/div[6]/div/div[2]/div[2]/div/div/div[2]/div/div/div[3]/button'

ADD_BUTTON_EXISTS_SINGLE = 'div[class="ddbc-collapsible__header-content-callout"]'
ADD_BUTTON_EXISTS_MANY = 'div[class="ct-equipment-shop__item-action"]'
ADD_TO_EQUIPMENT_BUTTON = 'ul[class="ct-character-sheet-MuiList-root ct-character-sheet-MuiList-padding""]'

MANAGE_EQUIPMENT = '/html/body/div[4]/div[2]/div/div[2]/div[3]/div/div[4]/div'
ADD_EQUIPMENT = '/html/body/div[5]/div[2]/div/div[2]/div[3]/div/div[4]'

ADD_CUSTOM_ITEM = 'a[class="ddbc-link  ddbc-theme-link"]'


CUSTOM_ITEM_INPUTS = 'div[class="ct-customize-data-editor__property-value"]'
CUSTOM_ITEM_QUANTITY = 'input[class="character-input ct-simple-quantity__input"]'

LOGIN = '#login-link'

USERNAME = '#login-username'
PASSWORD = '#password-input'

from typing import List, Dict, Union, NewType
# New Types
Chars = NewType('Chars', Dict[str, List[str]])
Update = NewType('Update', Dict[str, Union[str, float, int]])
