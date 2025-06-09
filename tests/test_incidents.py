def test_list_incidents(page, base_url):    
    page.goto(f"{base_url}/incident_list.do",  wait_until="networkidle")  
    assert "Incidents" in page.title() 
    page.screenshot(path="videos/incidents_list.png")
    
