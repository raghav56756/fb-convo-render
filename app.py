import asyncio
from playwright.async_api import async_playwright
import time

async def send_messages():
    with open("cookie.txt", "r") as f:
        raw = f.read().strip().split("\n")
        cookies = [{ "name": i.split("=")[0], "value": i.split("=")[1], "domain": ".facebook.com", "path": "/" } for i in raw]

    with open("uid.txt", "r") as f:
        uid = f.read().strip()

    with open("msgs.txt", "r", encoding="utf-8") as f:
        messages = f.read().strip().split("\n")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        await context.add_cookies(cookies)

        page = await context.new_page()
        await page.goto(f"https://mbasic.facebook.com/messages/read/?fbid={uid}")

        for msg in messages:
            try:
                await page.fill('textarea[name="body"]', msg)
                await page.click('input[name="send"]')
                print(f"✅ Sent: {msg}")
                time.sleep(5)
            except Exception as e:
                print(f"❌ Failed: {msg} - {e}")

        await browser.close()

asyncio.run(send_messages())
