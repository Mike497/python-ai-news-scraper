from openai import OpenAI

from config_util import ConfigUtil


class OpenAiUtil:

    def __init__(self):
        config = ConfigUtil().get_config()

        self.openai = OpenAI(
            api_key=config['openai']['api_key']
        )

        self.stop_word = "ERROR"

    def analyze_news_data(self, news_data):
        response = self.openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system",
                 "content": "You analyze given news and return back data in JSON format with field: news_tags. Detect what news data is passed and give short summary about the news as list of 5 tags (e.g. 'law, police, car, incidents, USA'). Content may come in any human language, respond accordingly. If no news can be found in the given data just respond with " + self.stop_word},
                {"role": "user", "content": "Analyze this news data: " + news_data}
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content

    def generate_embedding(self, text):
        response = self.openai.embeddings.create(
            model="text-embedding-ada-002",
            input=text
        )
        return response.data[0].embedding
