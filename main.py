from playwright.sync_api import Playwright, sync_playwright, expect
from dotenv import load_dotenv
import os

load_dotenv()

def check_status(page):
    html = page.locator('//*[@id="view"]/containers-view/div[2]/div/div/div/div/div/div[2]/table/tbody/tr[1]/td[3]/span').inner_html()
    if (html != 'healthy' or html != 'running'):
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
        page.locator('//*[@id="view"]/containers-view/div[2]/div/div/div/div/div/div[2]/table/tbody/tr[1]/td[1]/div/input').click()
        page.get_by_role("button", name="Restart").click()

    print("Closing.")

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
