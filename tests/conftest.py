# tests/conftest.py
import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
import pytest

load_dotenv()

AUTH_FILE = "playwright/.auth/state.json"

# tests/conftest.py
import os
from dotenv import load_dotenv
import pytest

load_dotenv()  # loads from .env by default

@pytest.fixture(scope="session")
def base_url():
    return os.getenv("SERVICENOW_BASE_URL")

@pytest.fixture(scope="session")
def credentials():
    return {
        "username": os.getenv("SERVICENOW_USERNAME"),
        "password": os.getenv("SERVICENOW_PASSWORD")
    }


def login_and_save_session():
    base_url = os.getenv("SERVICENOW_BASE_URL")
    username = os.getenv("SERVICENOW_USERNAME")
    password = os.getenv("SERVICENOW_PASSWORD")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            record_video_dir="videos/",
            viewport={"width": 1280, "height": 720}
        )
        page = context.new_page()
        page.goto(f"{base_url}")

        page.get_by_role("textbox", name="User name").click()
        page.get_by_role("textbox", name="User name").fill(username)
        page.get_by_role("textbox", name="User name").press("Tab")
        page.get_by_role("textbox", name="Password").fill(password)
        page.get_by_role("button", name="Log in").click()
        page.get_by_role("menuitem", name="All").click()

        # Wait until login completes and dashboard loads
        page.wait_for_url("**/ui_page.do**", timeout=10000)

        # Proceed with assertions or actions
        print("UI Page loaded")


        # Save storage state
        os.makedirs(os.path.dirname(AUTH_FILE), exist_ok=True)
        context.storage_state(path=AUTH_FILE)

        browser.close()

def pytest_sessionstart(session):
    # Only recreate session file if it's missing or empty
    if not os.path.exists(AUTH_FILE) or os.stat(AUTH_FILE).st_size == 0:
        print("[pytest] No login session found. Logging in to ServiceNow...")
        login_and_save_session()

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "storage_state": "playwright/.auth/state.json"
    }
