import os
import dotenv
import google.generativeai as genai


class Geminiflash:
    def __init__(self,sysprompt):
        dotenv.load_dotenv()
        self.jina_url = 'https://r.jina.ai/'
        with open(f"{sysprompt}.txt", "r") as f:
            self.sysprompt = f.read()
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY")
        genai.configure(api_key=self.gemini_api_key)
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash", system_instruction=self.sysprompt
        )

    def generate_response(self, jina_scrape):
        response = self.model.generate_content(jina_scrape)
        return response.text
