import os
import dotenv
import aiohttp
import google.generativeai as genai
import asyncio


class Cleanscraper:
    def __init__(self):
        dotenv.load_dotenv()
        self.jina_url = 'https://r.jina.ai/'
        with open("sysprompt_summary.txt", "r") as f:
            self.sysprompt_summary = f.read()
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY")
        genai.configure(api_key=self.gemini_api_key)
        self.summary_model = genai.GenerativeModel(
            model_name="gemini-1.5-flash", system_instruction=self.sysprompt_summary
        )


    async def simple_scrape(self, url):
        whole_url = self.jina_url + url
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(whole_url) as response:
                    return await response.text()
        except Exception as e:
            print(f"Failed to fetch {url}: {e}")
            return None

    def summarize_and_extract(self, jina_scrape):
        summary = self.summary_model.generate_content(jina_scrape)
        return summary.text
    
async def clean_scrape(url):
    scraper = Cleanscraper()
    jina_scrape = await scraper.simple_scrape(url)
    summary = scraper.summarize_and_extract(jina_scrape)
    return summary

async def main():
    print("Enter the URL to scrape:")
    url = input()
    summary = await clean_scrape(url)
    print(summary)


if __name__ == "__main__":
    asyncio.run(main())


