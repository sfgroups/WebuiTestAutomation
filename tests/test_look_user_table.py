# tests/test_login.py
def test_look_user_table(page, base_url):
    print("looking for the user list")
    page.goto(f"{base_url}/now/nav/ui/classic/params/target/sys_user_list.do%3Fsysparm_clear_stack%3Dtrue")
    # page.goto(f"{base_url}/sys_user_list.do")
    assert "ServiceNow" in page.title() 
    
    page.wait_for_timeout(3000)  # Wait 3 seconds for demo
    page.screenshot(path="videos/user_list.png")
    
