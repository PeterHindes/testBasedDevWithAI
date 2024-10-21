import asyncio
from pyppeteer import launch

prompt = 'what is the fastest way to sort a list of integers in python?'

async def main():
    browser = await launch(headless=False, executablePath='C:/Program Files/Google/Chrome/Application/chrome.exe', userDataDir='Default')  # Update this path to your Chrome executable
    page = await browser.newPage()
    await page.goto('https://chatgpt.com/?model=auto')  # Replace with the URL you want to visit

    # await asyncio.sleep(60)
    # set window size
    await page.setViewport({
        'width': 1920,
        'height': 1080
    })
    
    # wait to click on the bottom middle of the screen
    await asyncio.sleep(1)
    
    # click on the bottom middle of the screen
    # await page.mouse.click(960, 1080)
    
    # wait for the prompt to appear
    await asyncio.sleep(1)
    
    # press the keys of the prompt
    await page.keyboard.type(prompt, delay=50)
    
    # wait for the prompt to be typed
    await asyncio.sleep(1)
    
    # click the aria-label="Send prompt" button
    await page.click('button[aria-label="Send prompt"]')
    
    # Wait for some time to see the result
    await asyncio.sleep(60)

    # extract the outer html of this element from the page
    element = await page.querySelector('div[class="markdown"]')
    element_html = await page.evaluate('(element) => element.outerHTML', element)
    print(element_html)

    await browser.close()

asyncio.run(main())