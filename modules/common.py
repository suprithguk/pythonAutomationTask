import os, datetime
from random import choice
from modules import locators
from shutil import rmtree
import re, csv

# setup logs dirs
logs_dir = "logs"
screenshot_dir = "logs/screenshot/"
video_dir = "logs/videos/"
def check_and_create_dir(path: str) -> None:
    rmtree(path, ignore_errors=True)
    if not os.path.exists(path):
        os.mkdir(path)
check_and_create_dir(logs_dir)
check_and_create_dir(screenshot_dir)
check_and_create_dir(video_dir)

def get_timestamp() -> str:
    """
    Function to get te timestamp
    """
    return datetime.datetime.now().strftime("%d-%m-%y-%H-%M-%S")

def add_to_logs(logs, file_name="common_logs", display=True):
    
    """
    Function to dump all the logs in a file and on the console
    """

    with open(os.path.join("logs", file_name+".txt"), "a") as file:
        for x in logs.splitlines():
            if display: print(x)
            file.write(x+"\n")

def click_or_validate_element(page,
                              locator, 
                              method="get_by_role", 
                              wait=32000, 
                              take_screenshot=True,
                              click=True,
                              fill="",
                              select_element=None,
                              new_tab=False):

    """
    This function will do operations on web element.
    page : page object you want to interact with
    locator : this is the element id/xpath or value from locators.py
    method : how you want to find the locator get_by_label, locator, get_by_role, get_by_placeholder, get_by_text
    wait : want to wait before clicking the element
    wait_method : how you want to wait until visible until clock etc...
    take_screenshot : do you want to take screenshot before clicking
    click : do you want to click on the locator or not
    fill : what value you want to fill on the locator
    select_element: If a locator was a group of element then use the option to click on a specific number of element from the group pass random if you want to select random
    check: If you want to check the select button
    """

    page.wait_for_timeout(1000)
    element = ""
    try:
        if method == "get_by_label":
            if type(locator) == dict:
                element = page.get_by_label(locator.get("element"), name = locator.get("name") )
            else:
                element = page.get_by_label(locator)
        elif method == "locator":
            element = page.locator(locator)
        elif method == "get_by_placeholder":
            element = page.get_by_placeholder(locator)
        elif method == "get_by_text":
            element = page.get_by_text(locator, exact=True)
        else:
            element = page.get_by_role(locator.get("element"), name = locator.get("name"), exact=True )
    except :
        page.wait_for_timeout(1000)
        add_to_logs(f"Failed for element {locator}")
        page.screenshot(full_page=True, path=os.path.join(screenshot_dir, f"failed_{get_timestamp()}.png"))

    if select_element == "random":
        choice_value = choice(range(0, element.count()))
        add_to_logs(f"Selecting Value {choice_value} for element {locator} as {method}")
        element = element.nth(choice_value)
    elif select_element != None:
        element = element.nth(select_element)

    if click:
        add_to_logs(f"Clicking on {locator} as {method}")
        if new_tab:
            add_to_logs(f"opening the link in new_tab")
            with page.context.expect_page() as tab:
                element.click(timeout=wait)
                return tab
        else:
            element.click(timeout=wait)
    
    if take_screenshot: page.screenshot(full_page=True, path=os.path.join(screenshot_dir, f"{get_timestamp()}.png"))
    if fill: 
        element.fill(fill, timeout=wait)
        add_to_logs(f"Adding Value {fill} at element {locator} as {method}")

    return element

def extract_registration_numbers(file_path):
    """Extracts vehicle registration numbers from the input file."""
    with open(file_path, 'r') as file:
        content = file.read()

    # Regex pattern for UK registration numbers
    pattern = r'[A-Z]{2}[0-9]{2}\s?[A-Z]{3}'
    registrations = re.findall(pattern, content)

    # Normalize (remove spaces)
    return [reg.replace(" ", "") for reg in registrations]

def load_expected_output(file_path):
    """Load expected output from a CSV file."""
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]

def compare_results(actual, expected):
    """Compare actual and expected car details."""
    mismatches = []
    for actual_car in actual:
        matching_car = next(
            (car for car in expected if car["VARIANT_REG"] == actual_car["registration"]), 
            None
        )
        if not matching_car or any(
            actual_car[key] != matching_car[key] for key in ["make", "model", "year"]
        ):
            mismatches.append((actual_car, matching_car))
    return mismatches