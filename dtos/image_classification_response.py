from dataclasses import dataclass


@dataclass
class ImageClassificationResponse:
    image: str
    description: str
    predicted_class: str
    confidence: float
