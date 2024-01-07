import os

from flask import Flask, request, jsonify
from waitress import serve

from services import InstagramCrawlerService, ImageClassifierService

app = Flask(__name__)
instagram_crawler_service = InstagramCrawlerService()
image_classifier_service = ImageClassifierService()
UPLOAD_FOLDER = 'uploads'


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/search/<keyword>')
def search(keyword: str):
    images = instagram_crawler_service.crawl(keyword)
    return list(map(image_classifier_service.classify, images))


@app.route('/classify-image', methods=['POST'])
def classify_image():
    if 'image' not in request.files:
        return {'error': 'Missing \'image\' field.'}, 400

    image_file = request.files['image']

    if image_file.filename == '':
        return {'error': 'No \'image\' file selected.'}, 400

    if "image/" not in image_file.content_type:
        return {'error': '\'image\' must be an image type'}, 400

    # make OS specific path for the uploaded image
    image_path = os.path.join(UPLOAD_FOLDER, image_file.filename)
    # save image on path
    image_file.save(image_path)

    # classify image
    response = image_classifier_service.classify(image_path)
    # delete uploaded image
    os.remove(image_path)
    return jsonify(response)


if __name__ == '__main__':
    print('\nServer started on http://127.0.0.1:8080')
    serve(app, host='localhost', port=8080)
    print('\nServer stopped')
