# News Scraper App
This project is aimed to create a simple application in Python to sniff news from given HTML URLs, then storing them into internal DB with ability to search over saved news later.

## Prerequisites
1. Install Docker.
2. Run `docker-compose up -d` from root directory to start Pinecone vector DB locally.
3. Download Selenium webdriver for your OS.

## Setup
1. Install latest Python.
2. Use any favorite IDE (e.g. PyCharm) and import project there.
3. Run from Terminal in project's root: `pip install -r requirements.txt` to install necessary project's dependencies.
4. Set your api_key for OpenAI and path to downloaded Selenium webdriver in config.properties file.

## Run
Execute `main.py` Python script to launch the application. It can work in two modes:
1. Scraping news e.g. from habr.com. Pass command line arguments: `s https://habr.com/ru/articles/895800/ tm-title_h1 tm-article-body` to scrape an article, analyze via AI and store to vector DB. Where two last arguments are CSS classes on how to find article's header/body on the HTML page.
2. Querying news article via semantic search from Pinecone vector DB. Args example: `q AI ChatGPT OpenAI`. Params after `q` are tokens to search stored news for.
