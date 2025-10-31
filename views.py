from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import ImageUploadForm
from .models import ImageUpload
import tensorflow as tf
import numpy as np
import cv2
import os
from django.contrib.auth.models import User
from django.contrib import messages

def user_register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Account created successfully! You can now log in.")
        return redirect('login')

    return render(request, "register.html")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "paddy_project/models")

def load_model(model_name):
    model_path = os.path.join(MODELS_DIR, model_name)
    if os.path.exists(model_path):
        return tf.keras.models.load_model(model_path)
    else:
        print(f"Error: Model file '{model_name}' not found!")
        return None

cnn_model = load_model("cnn_model.h5")
resnet_model = load_model("resnet_model.h5")
efficient_model = load_model("efficientnet_model.h5")

CLASS_NAMES = ['Healthy', 'Pested']

def preprocess_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (128, 128))
    img = img / 255.0  # Normalize
    return np.expand_dims(img, axis=0)

def predict_image(image_path):
    img = preprocess_image(image_path)

    predictions = {}
    if cnn_model:
        predictions["CNN"] = cnn_model.predict(img)[0]  # Extract first row of predictions
    if resnet_model:
        predictions["ResNet"] = resnet_model.predict(img)[0]
    if efficient_model:
        predictions["EfficientNet"] = efficient_model.predict(img)[0]

    results = {}
    for model_name, prediction in predictions.items():
        predicted_class = np.argmax(prediction)  # Get index of max confidence
        confidence = round(float(np.max(prediction)) * 100, 2)  # Convert to percentage
        results[model_name] = (CLASS_NAMES[predicted_class], confidence)

    return results


@login_required
def home(request):
    return render(request, "home.html")

@login_required
def upload(request):
    return render(request, "upload.html")

@login_required
def upload_image(request):
    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_obj = form.save(commit=False)
            image_obj.user = request.user  # Assign the user
            image_obj.save()
            image_path = image_obj.image.path  # Get the uploaded image path

            results = predict_image(image_path)  # Get predictions from all models

            # Store predictions for all models in the database
            image_obj.predicted_class_cnn, image_obj.accuracy_cnn = results["CNN"]
            image_obj.predicted_class_resnet, image_obj.accuracy_resnet = results["ResNet"]
            image_obj.predicted_class_efficient, image_obj.accuracy_efficient = results["EfficientNet"]
            
            image_obj.save()

            return render(request, "result.html", {
                "image": image_obj,
                "results": results
            })

    form = ImageUploadForm()
    return render(request, "upload.html", {"form": form})

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')

    return render(request, "login.html")

def user_logout(request):
    logout(request)
    return redirect('login')
