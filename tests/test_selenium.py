import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
from time import sleep
import pytest

# Get the application URL from environment variable, or use default (localhost)
APP_URL = os.getenv("TODO_APP_URL", "http://localhost:80")

# Pytest fixture to set up and tear down the Chrome WebDriver
@pytest.fixture
def driver():
    chromedriver_autoinstaller.install()  # Automatically install ChromeDriver if needed
    options = Options()
    options.add_argument("--headless")  # Run in headless mode (no GUI)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

# First test: Add and delete a task called 'test123'
def test_site(driver):
    driver.get(APP_URL)
    sleep(1)

    # Check page title
    assert "Advanced Todo List" in driver.title

    # Find input field and submit a task
    search = driver.find_element(By.NAME, "task")
    search.send_keys("test123")
    search.send_keys(Keys.RETURN)
    sleep(1)

    # Verify task was added
    assert "test123" in driver.page_source

    # Find and delete the added task
    task_items = driver.find_elements(By.CLASS_NAME, "task-item")
    for task in task_items:
        if "test123" in task.text:
            delete_button = task.find_element(By.XPATH, ".//input[@type='submit' and @value='Delete']")
            delete_button.click()
            break
    sleep(1)
    # Verify task was deleted
    assert "test123" not in driver.page_source


# Second test: Add and delete a different task
def test_site2(driver):
    driver.get(APP_URL)
    sleep(1)

    assert "Advanced Todo List" in driver.title

    search = driver.find_element(By.NAME, "task")
    search.send_keys("test1234")
    search.send_keys(Keys.RETURN)
    sleep(1)

    assert "test1234" in driver.page_source

    task_items = driver.find_elements(By.CLASS_NAME, "task-item")
    for task in task_items:
        if "test1234" in task.text:
            delete_button = task.find_element(By.XPATH, ".//input[@type='submit' and @value='Delete']")
            delete_button.click()
            break
    sleep(1)
    assert "test1234" not in driver.page_source

