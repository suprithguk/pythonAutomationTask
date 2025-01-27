from fixtures import *
import os, yaml
from modules.common import video_dir
from pyvirtualdisplay import Display


@pytest.fixture(scope="session")
def config_data(request):

    config_file = "config.yaml"
    if os.environ.get("WEB_CONFIG"):
        config_file = os.environ.get("WEB_CONFIG")
    print(f"WEB_CONFIG set to {config_file}")
    with open(config_file, 'r') as file:
        data = yaml.safe_load(file)

    data["hide_browser"] = request.config.getoption("--hide_browser")
    return data

@pytest.fixture(scope="session")
def browser(config_data):

    if config_data.get("hide_browser"):
        display = Display(visible=0)
        display.start()
    with sync_playwright() as play_browser:
        browser = play_browser.firefox.launch(headless=False)
        yield browser
        browser.close()
    if config_data.get("hide_browser"): display.stop()

@pytest.fixture(scope="session")
def web_page(browser, request):
    if request.config.getoption("--record_video") == "yes":
        page = browser.new_page(record_video_dir=video_dir, no_viewport=True)
    else:
        page = browser.new_page()
    yield page
    page.close()
