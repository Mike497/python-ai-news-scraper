import json
import sys

from openai_util import OpenAiUtil
from pinecone_util import PineConeUtil
from selenium_util import SeleniumUtil

selenium_util = SeleniumUtil()
openai_util = OpenAiUtil()
pinecone_util = PineConeUtil()


def process_news_url(news_url, title_css_class_name, content_css_class_name):
    """
    Process news URL: scrape article's header/body, analyze via AI, store to vector DB (PineCone).

    Args:
        news_url (str): URL to a particular news article.
        title_css_class_name (str): CSS class on how to find news header in HTML page.
        content_css_class_name (str): CSS class on how to find news content in HTML page.

    Returns:
        str: Prints string with processing results.
    """
    try:
        print("Processing news URL:", news_url)
        print("")
        # Get the news title/content
        news_page_title, news_page_content = selenium_util.find_text_in_url_by_class(news_url, title_css_class_name,
                                                                                     content_css_class_name, 0)
        print("Scrapped news title:", news_page_title)
        print("")
        print("Scrapped news content:")
        print(news_page_content)

        # Analyze news via OpenAI completions API
        open_ai_news_analysis = openai_util.analyze_news_data(news_page_content)
        print("")
        open_ai_news_analysis_json = json.loads(open_ai_news_analysis)['news_tags']
        print("AI news analysis:", open_ai_news_analysis_json)

        # Store in vector DB (PineCone)
        embedding_vectors = openai_util.generate_embedding(open_ai_news_analysis_json)
        vectors_metadata = {
            "news_title": news_page_title,
            "news_content": news_page_content,
            "news_tags": open_ai_news_analysis_json
        }
        pinecone_util.insert_new_vectors(embedding_vectors, vectors_metadata)
        print("")
        print("Stored news processing result to vector DB")
    except:
        print("Exception occurred when processing news article, abort execution")
        exit(1)


def query_news_from_db(query_text):
    """
    Query vector DB data with news for given text.

    Args:
        query_text (str): Query text.

    Returns:
        str: Prints string with results that were found (top 3 results).
    """
    try:
        query_vector = openai_util.generate_embedding(query_text)
        query_result = pinecone_util.query_index(query_vector)
        print("")
        print("DB query result:", query_result)
    except:
        print("Exception occurred when querying the DB, abort execution")
        exit(1)


prog_mode = sys.argv[1]
if prog_mode == 's':
    process_news_url(sys.argv[2], sys.argv[3], sys.argv[4])
elif prog_mode == 'q':
    query_news_from_db(str(sys.argv[2:]))
exit(0)
