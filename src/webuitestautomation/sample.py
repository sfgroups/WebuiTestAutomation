from playwright.sync_api import sync_playwright

def select_combobox_option(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)

        # Locate the combo box
        combobox_locator = page.locator('#your-combobox-id')

        # Click to open the combo box
        combobox_locator.click()

        # Wait for the option to load
        page.locator('option', has_text='Not applicable').wait_for()

        # Select the 'Not applicable' option
        combobox_locator.select_option(label='Not applicable')


        browser.close()


if __name__ == '__main__':
    select_combobox_option('your_url')