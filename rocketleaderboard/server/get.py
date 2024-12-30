import asyncio
import json
import argparse
from playwright.async_api import async_playwright


async def main():
    parser = argparse.ArgumentParser(
        description="Scrape a URL and capture API responses."
    )
    parser.add_argument(
        '--url',
        required=True,
        help='URL to visit',
    )
    args = parser.parse_args()

    async with async_playwright() as p:
        browser = await p.chromium.launch(args=['--no-sandbox'])
        page = await browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/83.0.4103.116 Safari/537.36"
        )

        await page.set_extra_http_headers({"Accept-Language": "en"})

        async def handle_response(response):
            if "api.tracker.gg/api" not in response.url:
                return
            try:
                data = await response.json()
                print(json.dumps(data))
                # Uncomment and modify the lines below to save data to a file
                # filename = args.filename or "response"
                # with open(f"/tmp/{filename}.json", "w") as f:
                #     json.dump(data, f)
            except Exception as e:
                print(e)
                exit(5)

        page.on("response", handle_response)

        await page.goto(args.url, wait_until="networkidle")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
