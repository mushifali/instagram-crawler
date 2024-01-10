## instagram-crawler

This is an instagram crawler API that crawls the instagram website to extract images that match a keyword. It also uses
a pretrained `imagenet` ML model to classify the images.

### Project Setup:

This project requires Python 3. I have used `Python 3.11.7` for development. It uses the following
libraries: `flask, waitress, selenium, tensorflow, keras` etc.

To install dependencies run the following command:

```bash
pip install -r requirements.txt
```

To start the project, run the following command:

```bash
python app.py
```

It will start the `flask` project on http://localhost:8080.

> **Note**: This project assumes that you have Chrome browser installed on your machine. It might take a couple of minutes to startup for the first time because it downloads the latest chrome driver and `imagenet` pre-trained ML dataset. However, subsequent startups would be instantaneous.

### API Endpoints:

- **Search `GET /search/<keyword>`**

This `GET` endpoint expects a `keyword` as a path variable. It crawls the Instagram
website: https://www.instagram.com/explore/tags/keyword using `selenium` (with the latest chrome driver) and extracts the top 5 images. Then it
uses `tensorflow/keras` library to run the pre-trained `imagenet` ML model to classify the image.

Here is a sample `curl` request:

```bash
curl --location 'localhost:8080/search/fruit'
```

Here is the sample response:

```json
[
  {
    "confidence": 82.61,
    "description": "This image contains a 'pomegranate' with 82.61% confidence score.",
    "image": "https://instagram.fisb9-1.fna.fbcdn.net/v/t51.2885-15/416429664_1358003884832081_4198775704033250456_n.jpg?stp=dst-jpg_e35_p1080x1080&_nc_ht=instagram.fisb9-1.fna.fbcdn.net&_nc_cat=105&_nc_ohc=CuO-SF3oSwcAX8WRwfB&edm=AOUPxh0BAAAA&ccb=7-5&oh=00_AfDLXguT7WW-B5gGdu1UPe7kPD7RziAzWcK_orGBgqVPPw&oe=659F25AE&_nc_sid=9dc660",
    "predicted_class": "pomegranate"
  },
  {
    "confidence": 51.41,
    "description": "This image contains a 'corn' with 51.41% confidence score.",
    "image": "https://instagram.fisb9-1.fna.fbcdn.net/v/t51.2885-15/417399303_674455781426843_7800404223257519104_n.jpg?stp=dst-jpg_e35_p1080x1080&_nc_ht=instagram.fisb9-1.fna.fbcdn.net&_nc_cat=111&_nc_ohc=AoqPpdu-h24AX8LSpuC&edm=AOUPxh0BAAAA&ccb=7-5&oh=00_AfC8MkPtvEs6n438eDm1OD-eT_XCXm5AOIqPvn0ZVpUfJQ&oe=659F22CB&_nc_sid=9dc660",
    "predicted_class": "corn"
  },
  {
    "confidence": 44.69,
    "description": "This image contains a 'plate' with 44.69% confidence score.",
    "image": "https://instagram.fisb9-1.fna.fbcdn.net/v/t51.2885-15/416698970_280283371367648_4997356792264660874_n.jpg?stp=c0.135.1080.1080a_dst-jpg_e35_s640x640_sh0.08&_nc_ht=instagram.fisb9-1.fna.fbcdn.net&_nc_cat=108&_nc_ohc=RPcOpjx465sAX8We9qh&edm=AOUPxh0BAAAA&ccb=7-5&oh=00_AfD8-bM9QC_Vjy-GD14bF7Dym8jQNNlh3Qw0zT1SUX01dA&oe=65A02D55&_nc_sid=9dc660",
    "predicted_class": "plate"
  },
  {
    "confidence": 67.98,
    "description": "This image contains a 'comic book' with 67.98% confidence score.",
    "image": "https://instagram.fisb9-1.fna.fbcdn.net/v/t51.2885-15/417222381_331734743061659_5925629921011415964_n.jpg?stp=c0.53.538.538a_dst-jpg_e35&_nc_ht=instagram.fisb9-1.fna.fbcdn.net&_nc_cat=1&_nc_ohc=8_UBKHI-uXUAX_TL91O&edm=AOUPxh0BAAAA&ccb=7-5&oh=00_AfBEf9HPTR1n07wEyFzvJpWl4JmfKnTmRIrr9Q5TLan7bg&oe=659F6614&_nc_sid=9dc660",
    "predicted_class": "comic book"
  },
  {
    "confidence": 50.01,
    "description": "This image contains a 'ice cream' with 50.01% confidence score.",
    "image": "https://instagram.fisb9-1.fna.fbcdn.net/v/t51.2885-15/417544206_1631529237653057_1123879080744865644_n.jpg?stp=dst-jpg_e35_p1080x1080&_nc_ht=instagram.fisb9-1.fna.fbcdn.net&_nc_cat=105&_nc_ohc=ZdSzVV5Q-rEAX-1Q4L7&edm=AOUPxh0BAAAA&ccb=7-5&oh=00_AfCjPgz5Cn75rtYZlxkyOkFmVCrcCptSxVNR_lilLRTEbw&oe=659FF8DD&_nc_sid=9dc660",
    "predicted_class": "ice cream"
  }
]
```

- **Classify Image `POST /classify-image`**

This `POST` endpoint allows to run the pre-trained `imagenet` ML model on an uploaded image. It expects `image`
form-data field which would be an image file. It uses `tensorflow` library to run the pre-trained `imagenet` ML model to
classify the image.

Here is a sample `curl` request:

```bash
# Download the 'lion.jpg' file
wget -O lion.jpg https://images.rawpixel.com/image_800/cHJpdmF0ZS9sci9pbWFnZXMvd2Vic2l0ZS8yMDIzLTA4L3Jhd3BpeGVsX29mZmljZV8yX3Bob3RvX29mX2FfbGlvbl9pc29sYXRlZF9vbl9jb2xvcl9iYWNrZ3JvdW5kXzJhNzgwMjM1LWRlYTgtNDMyOS04OWVjLTY3ZWMwNjcxZDhiMV8xLmpwZw.jpg
# Send the 'lion.jpg' file
curl --location 'localhost:8080/classify-image' --form  image=@lion.jpg
```

Here is the sample response:

```json
{
  "confidence": 89.61,
  "description": "This image contains a 'lion' with 89.61% confidence score.",
  "predicted_class": "lion"
}
```