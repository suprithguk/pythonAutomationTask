# **Car Valuation E2E Test Suite**
  This project is an end-to-end (E2E) automation test suite designed to validate vehicle details fetched from a car valuation website against expected results.

  The framework uses Python, Playwright and is set up for seamless integration with Jenkins.

---

 # Setup

 Setup a virtual env and install playwright.

 ```
 git clone https://github.com/suprithguk/seleniumPythonTask.git; cd seleniumPythonTask
 Unzip following file: lib/python3.13/site-packages/playwright/driver/node.zip
 python -m venv py_env
 source py_env/bin/activate
 pip install -r requriments.txt
 playwright install
 ```

# How To Run Test Case

```
pytest tests/test.py --junitxml=results.xml.xml --hide_browser
```
