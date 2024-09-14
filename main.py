import json
from tqdm import tqdm
from playwright.sync_api import sync_playwright


HOME_PAGE = "https://finnotech.ir/doc/"


if __name__ == '__main__':
    result = []

    # Start Playwright and open a browser
    with sync_playwright() as p:
        # You can set headless=False to see the browser window
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Navigate to the desired webpage
        page.goto(HOME_PAGE)

        # Get only the visible text content from the page
        visible_text = page.evaluate('document.body.innerText')
        result.append(visible_text)

        # Get all the links on the page
        anchors = page.locator('xpath=//table//a')

        # Extract the href attribute for each link
        links = []
        for i in range(anchors.count()):
            link = anchors.nth(i)
            links.append(HOME_PAGE + link.get_attribute("href"))

        # Print the list of links
        for link in tqdm(links):
            page.goto(link)
            # Get only the visible text content from the page
            visible_text = page.evaluate('document.body.innerText')
            result.append(visible_text)

        # Close the browser
        browser.close()

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
