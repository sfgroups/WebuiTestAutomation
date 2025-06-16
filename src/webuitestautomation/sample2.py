from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    
    # Navigate to your page
    page.goto("https://your-servicenow-url.com")

    # Click the combo box
    page.click("css=YOUR_COMBOBOX_SELECTOR")  # Update selector

    # Wait for the options to load (you can wait for an option with text "Not applicable")
    page.wait_for_selector("text=Not applicable")

    # Click the option
    page.click("text=Not applicable")

    # Optional: verify selection or proceed with next steps
    # e.g., page.click("css=button:has-text('Submit')")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)
