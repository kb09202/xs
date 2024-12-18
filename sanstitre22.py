# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 20:42:43 2024

@author: pc
"""

import cv2
import numpy as np
import tensorflow as tf

# Charger un modèle pré-entraîné DeepLabV3+
model = tf.keras.applications.DenseNet201(weights="imagenet", include_top=False)

# Prétraitement de l'image
def preprocess_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (224, 224))
    img = tf.keras.applications.densenet.preprocess_input(img)
    return img

# Segmenter l'image
def segment_image(image_path):
    img = preprocess_image(image_path)
    img = np.expand_dims(img, axis=0)
    predictions = model.predict(img)
    segmentation = tf.argmax(predictions, axis=-1).numpy()[0]
    return segmentation

image_path = "road_image.jpg"
segmentation = segment_image(image_path)

cv2.imshow("Segmentation", (segmentation * 255).astype('uint8'))
cv2.waitKey(0)
cv2.destroyAllWindows()
