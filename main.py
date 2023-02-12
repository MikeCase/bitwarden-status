from playwright.sync_api import Playwright, sync_playwright, expect
from dotenv import load_dotenv
import os

load_dotenv()

def check_status(page):
    html = page.inner_html('span.label')
    if (html != 'healthy'):
        return False
    else:
        return True


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True, slow_mo=300)
    context = browser.new_context()
    page = context.new_page()
    page.goto(os.getenv("LOGIN_URL"))

    # Login to portainer to check the status of bitwarden. 
    print("Logging in..@URL " + os.getenv("LOGIN_URL"))
    page.wait_for_load_state('networkidle')
    page.get_by_placeholder("Enter your username").fill(os.getenv("USERNAME"))
    page.get_by_placeholder("Enter your password").fill(os.getenv("PASSWORD"))
    page.get_by_role("button", name="Login").click()

    print("Going to dashboard...@URL " + os.getenv("DASHBOARD_URL"))
    page.wait_for_load_state('networkidle')
    # Goto the dashboard
    page.goto(os.getenv("DASHBOARD_URL"))
    page.wait_for_load_state('networkidle')
    # Load the containers list.
    page.get_by_role("link", name="Container", exact=True).click()
    page.wait_for_load_state('networkidle')

    # Check the status of the bitwarden server.
    print("Checking status of bitwarden on server.")
    if check_status(page):
        print("Server is healthy.") # Good Continue
    else:
        print("Server unhealthy restarting bitwarden..") # Not good, restart bitwarden. 
        page.get_by_role("row", name="Click to select this row bitwarden_bitwarden_1 healthy Logs Inspect Stats Exec Console Attach Console bitwarden docker.io/vaultwarden/server:latest 2022-05-01 23:45:14 172.18.0.2 none 8088:80 administrators").get_by_role("checkbox", name="Click to select this row").check()
        page.get_by_role("button", name="Restart").click()
        
    print("Closing.")

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
