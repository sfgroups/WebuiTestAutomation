# tests/test_dashboard.py
def test_dashboard(page, base_url):
    page.goto(base_url)
    page.wait_for_timeout(2000) 
    assert "ServiceNow" in page.title()
