import sys, asyncio
from playwright.async_api import async_playwright
async def main(html, pdf, png=None):
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        await pg.goto('file://' + html); await pg.wait_for_timeout(800)
        await pg.pdf(path=pdf, prefer_css_page_size=True, print_background=True)
        await b.close()
asyncio.run(main(*sys.argv[1:]))
