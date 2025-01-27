from fixtures import *
from modules import common, locators
import re

def test_01(web_page, config_data):
    web_page.goto('https://www.webuyanycar.com/')
    reg_num = common.extract_registration_numbers(config_data.get('inputFile'))
    output_data = common.load_expected_output(config_data.get('outputFile'))
    common.click_or_validate_element(web_page, locators.accept_cookies, method='locator')
    for x in reg_num:
        common.click_or_validate_element(web_page, locators.searchBox, fill=x, method='get_by_placeholder')
        common.click_or_validate_element(web_page, locators.mileage, fill="1000", method='locator')
        common.click_or_validate_element(web_page, locators.searchButton, method='locator')
        # try:
        #     common.click_or_validate_element(web_page, locators.sorryText, method='locator', click=False)
        #     web_page.reload()
        # except:
        #     pass
        # common.click_or_validate_element(web_page, locators.searchButton, select_element=2)
        data = common.click_or_validate_element(web_page, locators.car_details, method='locator', select_element=0, click=False).inner_html()
        common.add_to_logs(data)
        print(output_data)
        common.click_or_validate_element(web_page, locators.backButton, method='locator')
        match = re.search(r"Registration Number (\w+)", str(output_data))
        if match:
            reg_number = match.group(1)  # Extracted registration number
        else:
            print("No registration number found in the string.")
            exit()