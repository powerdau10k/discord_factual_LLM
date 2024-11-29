from cleanscrape import Cleanscraper
import google.generativeai as genai
from googleapiclient.discovery import build
from geminiflash import Geminiflash 
import asyncio
import os

def final_response(question,summaries,promptname):     
    gemflash =  Geminiflash("final_answer")
    response = gemflash.generate_response(str(summaries))
    return response


async def get_facts(question):
    summaries = []
    scraper = Cleanscraper()
    query = formulate_response(question,"question2query")
    links = return_links(query)
    for link in links:
        jina_scrape = await scraper.simple_scrape(link)
        summary = scraper.summarize_and_extract(jina_scrape)
        summ_dict = {"link": link, "summary": summary}
        summaries.append(summ_dict)
    return summaries


def formulate_response(LLMInput,promptname):
    gemflash = Geminiflash(promptname)
    response = gemflash.generate_response(LLMInput)
    return response


def return_links(query):
    google_cse_id = os.getenv("GOOGLE_CSE_ID")
    google_cse_api_key = os.getenv("GOOGLE_CSE_API_KEY")
    service = build("customsearch", "v1", developerKey=google_cse_api_key)
    res = service.cse().list(q=query, cx=google_cse_id, num=5).execute()
    links = extract_hyperlinks(res)
    return links

def extract_hyperlinks(cse_response):
    items = cse_response.get("items", [])
    links = [item["link"] for item in items if "link" in item]
    return links

async def answer_question(question):
    summaries = await get_facts(question)
    response = final_response(question,summaries,"final_answer")
    return response

def main():
    print("Enter question:")
    question = input()
    summaries = asyncio.run(get_facts(question))
    response = final_response(question,summaries,"final_answer")
    print(response)
    
if __name__ == "__main__":
    main()
