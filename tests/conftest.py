# tests/conftest.py
import os
import time
import shutil
import pytest
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page

AUTH_FILE = "playwright/.auth/state.json"
VIDEO_DIR = "videos/"

# Global shared objects
playwright = None
browser: Browser = None
context: BrowserContext = None

load_dotenv()

@pytest.fixture(scope="session")
def base_url():
    url = os.getenv("SERVICENOW_BASE_URL")
    print(f"[DEBUG] Loaded base_url: {url}")
    if not url:
        raise RuntimeError("Environment variable SERVICENOW_BASE_URL is missing.")
    return url



def remove_if_older_than_1_hour(file_path):
    if os.path.exists(file_path):
        age = time.time() - os.path.getmtime(file_path)
        if age > 3600:
            os.remove(file_path)
            print(f"Removed old auth file: {file_path}")


def login_and_save_session():
    global playwright, browser, context

    base_url = os.getenv("SERVICENOW_BASE_URL")
    username = os.getenv("SERVICENOW_USERNAME")
    password = os.getenv("SERVICENOW_PASSWORD")

    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(
        record_video_dir=VIDEO_DIR,
        viewport={"width": 1280, "height": 720}
    )
    page = context.new_page()
    page.goto(base_url)

    page.get_by_role("textbox", name="User name").fill(username)
    page.get_by_role("textbox", name="Password").fill(password)
    page.get_by_role("button", name="Log in").click()
    page.get_by_role("menuitem", name="All").click()

    page.wait_for_url("**/ui_page.do**", timeout=10000)

    os.makedirs(os.path.dirname(AUTH_FILE), exist_ok=True)
    context.storage_state(path=AUTH_FILE)


@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    global playwright, browser, context

    remove_if_older_than_1_hour(AUTH_FILE)

    if not os.path.exists(AUTH_FILE) or os.stat(AUTH_FILE).st_size == 0:
        print("[pytest] Logging in to ServiceNow...")
        login_and_save_session()
    else:
        print("[pytest] Reusing existing session...")
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context(
            storage_state=AUTH_FILE,
            record_video_dir=VIDEO_DIR,
            viewport={"width": 1280, "height": 720}
        )


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    global context, browser, playwright
    if context:
        context.close()
    if browser:
        browser.close()
    if playwright:
        playwright.stop()


@pytest.fixture(scope="function")
def page(request) -> Page:
    global context
    if not context:
        raise RuntimeError("Playwright context was not initialized.")

    page = context.new_page()
    yield page

    if page.video:
        video_path = page.video.path()
        test_name = request.node.name.replace(" ", "_")
        new_path = os.path.join(VIDEO_DIR, f"{test_name}.webm")
        page.close()
        shutil.move(video_path, new_path)
        print(f"[Video saved] {new_path}")
    else:
        page.close()
