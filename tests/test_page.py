def test_example(page):
    page.goto("https://www.google.com/")
    assert "Google" in page.title()
