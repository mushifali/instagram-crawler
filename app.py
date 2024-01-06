from flask import Flask
from waitress import serve

from services import InstagramCrawlerService, ImageClassifierService

app = Flask(__name__)
instagram_crawler_service = InstagramCrawlerService()
image_classifier_service = ImageClassifierService()


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/search/<keyword>')
def search(keyword: str):
    images = instagram_crawler_service.crawl(keyword)
    return list(map(image_classifier_service.classify, images))


if __name__ == '__main__':
    print('\nServer started on http://127.0.0.1:8080')
    serve(app, host='localhost', port=8080)
    print('\nServer stopped')
