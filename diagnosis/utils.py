import os
import tensorflow as tf
import tensorflow_hub as hub
import tf_keras as tfk
import numpy as np
from config import settings

def user_directory_path(instance, filename):
    return f'xrays/user_{instance.user.id}/{filename}'

# PSI --------------------------

def calculate_psi_score(data):
    score = 0

    if data.gender == 'M':
        score += data.age
    else:
        score += (data.age - 10)

    if data.nursing_home: score += 10

    if data.cancer: score += 30
    if data.liver_disease: score += 20
    if data.heart_disease: score += 10
    if data.cerebrovascular_disease: score += 10
    if data.renal_disease: score += 10

    if data.altered_mental_status: score += 20
    if data.respiratory_rate >= 30: score += 20
    if data.systolic_bp < 90: score += 20
    if data.temperature < 35 or data.temperature >= 40: score += 15
    if data.pulse >= 125: score += 10

    if data.hemoglobin < 100:
        score += 10

    return score

# X-Ray --------------------------

def get_risk_class(score):
    if score <= 50:
        return "I (Низький)", "0.1%"
    elif score <= 70:
        return "II (Низький)", "0.6%"
    elif score <= 90:
        return "III (Середній)", "0.9 - 2.8%"
    elif score <= 130:
        return "IV (Високий)", "8.2 - 9.3%"
    else:
        return "V (Дуже високий)", "27 - 31%"

def load_model(model_path):
    print(f"Loading saved model from: {model_path}...")
    model = tfk.models.load_model(model_path,
                                custom_objects={"KerasLayer": hub.KerasLayer})
    return model

def process_image(image_path, img_size=224):
    """
    Turns the image into a Tensor.
    """
    image = tf.io.read_file(image_path)
    image = tf.image.decode_jpeg(image, channels=3)
    image = tf.image.convert_image_dtype(image, tf.float32)
    image = tf.image.resize(image, size = [img_size, img_size])

    return image

def get_image_label(image_path, label):
  return process_image(image_path), label

def create_data_batches(X, y=None, batch_size=32, valid_data=False, test_data=False):
    if test_data:
        print("Creating test data batches...")
        data = tf.data.Dataset.from_tensor_slices((tf.constant(X)))
        data_batch = data.map(process_image).batch(batch_size)
        return data_batch
    elif valid_data:
        print("Creating validation data batches...")
        data = tf.data.Dataset.from_tensor_slices((tf.constant(X),
                                                   tf.constant(y)))
        data_batch = data.map(get_image_label).batch(batch_size)
        return data_batch
    else:
        print("Creating training data batches...")
        data = tf.data.Dataset.from_tensor_slices((tf.constant(X),
                                                   tf.constant(y)))
        data = data.shuffle(buffer_size=len(X))
        data = data.map(get_image_label)
        data_batch = data.batch(batch_size)
    return data_batch

def get_pred_label(preds):
    """
    Turns an array of prediction probabilities into a label.
    """
    labels = ['normal', 'pneumonia']
    classes = np.unique(labels)
    return classes[np.argmax(preds)]

MODEL_PATH = os.path.join(settings.BASE_DIR, 'diagnosis', 'models', '20260122-06061769064826-full-model-mobilenetv2-Adam.h5')

print("Завантаження ML моделі...")
try:
    AI_MODEL = load_model(MODEL_PATH)
    print("Модель успішно завантажена!")
except Exception as e:
    print(f"Не вдалося завантажити модель: {e}")
    AI_MODEL = None

def calculate_xray_probability(img_path):
    if AI_MODEL is None:
        return "Model Error", 0.0
    data = create_data_batches([img_path], test_data=True)

    prediction = AI_MODEL.predict(data)
    label = get_pred_label(prediction[0])
    probability = np.max(prediction) * 100

    return label, probability
