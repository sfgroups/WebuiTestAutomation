# tests/test_login.py
def test_look_user_table(page, base_url):
    print("looking for the user list")
    page.goto(f"{base_url}/sys_user_list.do",  wait_until="networkidle")       
    assert "Users" in page.title() 
    page.screenshot(path="videos/user_list.png")
    
