from flask import Flask, request, jsonify  # Untuk membuat API
from flask_cors import CORS  # Untuk mengaktifkan CORS
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras import layers, Model
from PIL import Image
import numpy as np
from io import BytesIO
import os

# Inisialisasi aplikasi Flask
app = Flask(__name__)

# Aktifkan CORS agar API bisa diakses dari berbagai domain
CORS(app)

# Load model yang sudah dilatih
try:
    # Coba load model yang ada
    model = load_model("model_gbk_new.keras", compile=False, safe_mode=False)
    print("✓ Model loaded successfully!")
except Exception as e:
    # Jika gagal, buat model baru dengan arsitektur yang sama
    print(f"✗ Error loading saved model: {str(e)}")
    print("🔄 Creating new model with MobileNetV2 architecture...")
    
    # Buat model baru dengan arsitektur yang benar
    base_model = MobileNetV2(include_top=False, input_shape=(160, 160, 3), weights='imagenet')
    base_model.trainable = False
    
    inputs = tf.keras.Input(shape=(160, 160, 3))
    x = base_model(inputs, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dense(256, activation='relu')(x)
    x = layers.Dropout(0.5)(x)
    outputs = layers.Dense(3, activation='softmax')(x)
    
    model = Model(inputs, outputs)
    print("⚠ WARNING: Using untrained model! Please train and save a new model.")
    print("⚠ Predictions may not be accurate.")

# Label yang digunakan sesuai dengan model yang dilatih
LABELS = ['paper', 'rock', 'scissors']

# Route untuk halaman utama API
@app.route('/')
def welcome():
    return jsonify({"message": "Selamat Datang di API Model Gambar Permainan Tangan Gunting, Batu dan Kertas"}), 200  # Response untuk halaman utama

# Route untuk prediksi gambar
@app.route('/predict', methods=['POST'])
def predict():
    # Pastikan ada file yang diunggah melalui request
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']  # Mengambil file dari request

    try:
        # Preprocessing gambar
        image = Image.open(BytesIO(file.read()))  # Membaca file sebagai stream gambar
        image = image.resize((160, 160))         # Mengubah ukuran gambar sesuai input model
        image = img_to_array(image)              # Konversi gambar ke array numpy
        image = np.expand_dims(image, axis=0)    # Tambahkan dimensi batch untuk input model
        image = image / 255.0                    # Normalisasi piksel gambar ke rentang [0, 1]

        # Prediksi menggunakan model
        prediction = model.predict(image)  # Menghasilkan probabilitas untuk setiap kelas
        predicted_class = LABELS[np.argmax(prediction)]  # Mengambil label dengan probabilitas tertinggi
        confidence = float(np.max(prediction))  # Confidence dari prediksi

        # Response hasil prediksi
        return jsonify({
            "prediction": predicted_class,  # Label hasil prediksi
            "confidence": confidence        # Confidence level
        }), 200
    except Exception as e:
        # Jika terjadi kesalahan dalam proses, berikan error
        return jsonify({"error": f"Error processing image: {str(e)}"}), 500

# Jalankan aplikasi Flask
if __name__ == '__main__':
    app.run(debug=True)  # Mode debug diaktifkan untuk pengembangan
