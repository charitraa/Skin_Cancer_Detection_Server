# predictor.py
import numpy as np
from tensorflow.keras.models import load_model # type: ignore # 
from tensorflow.keras.preprocessing import image # type: ignore
from PIL import Image

class SkinCancerPredictor:
    def __init__(self, model_path="./models/skin_cancer_cnn.h5"):
        self.model = load_model(model_path)

    def predict(self, img: Image.Image):
        # Preprocess image
        img = img.resize((224, 224))
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # Predict
        prediction = self.model.predict(img_array)
        class_label = "Malignant" if prediction > 0.5 else "Benign"
        confidence_score = float(prediction[0][0])

        return class_label, confidence_score
