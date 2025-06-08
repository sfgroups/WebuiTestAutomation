# tests/test_dashboard.py
def test_dashboard(page, base_url):
    page.goto(base_url)
    assert "ServiceNow" in page.title()
