pytest_plugins = [
   "fixtures.engine",
]

def pytest_addoption(parser):
   parser.addoption("--record_video", action="store", default="yes", help="Use this flag to record the video if yes it will else it wont.")
   parser.addoption("--hide_browser", action="store_true", default=False, help="Use this flag if you want to hide the browser it's like headless run.")
