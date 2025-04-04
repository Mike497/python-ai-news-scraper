import asyncio
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

        # Analyze news via OpenAI completions API (with chunking support)
        open_ai_news_analysis = []
        if openai_util.count_tokens(news_page_content) < openai_util.tokens_limit:
            open_ai_news_analysis = openai_util.get_ai_completion_response(news_page_content)
        else:
            news_chunks = openai_util.split_data_into_chunks(news_page_content, openai_util.tokens_limit)
            results = asyncio.run(parallel_openai_completions_calls(news_chunks))
            open_ai_news_analysis = [item for sublist in results for item in sublist]  # flatten list

        print("")
        print("AI news analysis:", open_ai_news_analysis)

        # Store in vector DB (PineCone)
        embedding_vectors = openai_util.generate_embedding(open_ai_news_analysis)
        vectors_metadata = {
            "news_title": news_page_title,
            "news_content": news_page_content,
            "news_tags": open_ai_news_analysis
        }
        pinecone_util.insert_new_vectors(embedding_vectors, vectors_metadata)
        print("")
        print("Stored news processing result to vector DB")
    except:
        print("Exception occurred when processing news article, abort execution")
        exit(1)


# Util method to make async calls to OpenAI completions API
async def parallel_openai_completions_calls(news_chunks):
    return await openai_util.run_parallel_openai_completions_calls(news_chunks)


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
