import asyncio
import json

import tiktoken
from openai import OpenAI

from config_util import ConfigUtil


class OpenAiUtil:

    def __init__(self):
        config = ConfigUtil().get_config()

        self.openai = OpenAI(
            api_key=config['openai']['api_key']
        )

        self.stop_word = "ERROR"
        self.tokens_limit = 500  # for a purpose to test chunks

    def count_tokens(self, text, model="gpt-4o-mini"):
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))

    async def run_parallel_openai_completions_calls(self, news_chunks):
        tasks = [asyncio.to_thread(self.get_ai_completion_response, news_chunk) for news_chunk in news_chunks]
        results = await asyncio.gather(*tasks)
        return results

    def get_ai_completion_response(self, news_data):
        response = self.openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system",
                 "content": "You analyze given news and return back data in JSON format with field: news_tags. Detect what news data is passed and give short summary about the news as list of 5 tags (e.g. 'law, police, car, incidents, USA'). Content may come in any human language, respond accordingly. If no news can be found in the given data or you do not understand text just respond with " + self.stop_word},
                {"role": "user", "content": "Analyze this news data: " + news_data}
            ],
            temperature=0.7,
        )
        ai_response = response.choices[0].message.content
        if ai_response == self.stop_word:
            return []
        return json.loads(ai_response)['news_tags']

    def split_data_into_chunks(self, data, chunk_size):
        chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
        return chunks

    def generate_embedding(self, text):
        response = self.openai.embeddings.create(
            model="text-embedding-ada-002",
            input=text
        )
        return response.data[0].embedding
