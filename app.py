from flask import Flask
from waitress import serve

from services.instagram_crawler_service import InstagramCrawlerService

app = Flask(__name__)
instagram_crawler_service = InstagramCrawlerService()


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/search/<keyword>')
def search(keyword: str):
    return instagram_crawler_service.crawl(keyword)


if __name__ == '__main__':
    serve(app, host='localhost', port=8080)
