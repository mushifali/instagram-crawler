from io import BytesIO

import numpy as np
import requests
from PIL import Image
from keras.applications.xception import Xception
from keras.applications.xception import preprocess_input, decode_predictions
from keras.preprocessing import image

from dtos import ImageClassificationResponse


class ImageClassifierService:
    """
    Image classifier Service - to classify images using a pre-trained imagenet model.
    """
    def __init__(self):
        # load the model
        self.model = Xception(weights='imagenet', include_top=True)

    def classify(self, image_path: str) -> ImageClassificationResponse:
        """
        Classifies an image using the pre-trained imagenet model.

        :param image_path: path of the image to classify
        :return: image classification
        """
        # get the image
        if image_path.startswith('https://'):
            response = requests.get(image_path)
            img = Image.open(BytesIO(response.content))
        else:
            # load image from local path
            img = image.load_img(image_path)

        # resize the image according to imagenet model's requirement
        img = img.resize((299, 299))

        # convert to numpy array and do preprocessing
        np_array = image.img_to_array(img)
        np_array = np.expand_dims(np_array, axis=0)
        np_array = preprocess_input(np_array)

        # predict features from the numpy array
        features = self.model.predict(np_array)
        predicted_features = decode_predictions(features)[0][0]

        # prepare response
        predicted_class = predicted_features[1].replace('_', ' ')
        confidence = round(predicted_features[2] * 100, 2)
        description = f'This image contains a \'{predicted_class}\' with {confidence:.2f}% confidence score.'

        return ImageClassificationResponse(
            image_path if image_path.startswith('https://') else 'N/A',
            description,
            predicted_class,
            confidence
        )
