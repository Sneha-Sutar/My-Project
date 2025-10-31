🧠 Paddy Yield and Quality Analysis using Deep Learning

A smart image-based system that detects whether a paddy crop is healthy or pest-affected using CNN, ResNet, and EfficientNet models.

🚀 How It Works

User uploads a paddy image.

Image is preprocessed and analyzed by three AI models.

System predicts: Healthy 🌾 or Pested 🐛.

Results are stored in the database.

🧩 Tech Stack

Python | Django | TensorFlow | Keras | OpenCV | HTML | CSS | SQLite

⚙️ Model Accuracy

CNN: 84.07%

ResNet: 75.89%

EfficientNet: 82.96%

🖥️ How to Run

* Install dependencies:

pip install django pillow tensorflow keras numpy opencv-python


* Run migrations:

python manage.py makemigrations
python manage.py migrate


* Start the server:

python manage.py runserver

💡 About

This system helps farmers and researchers quickly analyze crop health and prevent yield losses.
