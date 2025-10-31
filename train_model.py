import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import ResNet50, EfficientNetB0
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D
from tensorflow.keras.optimizers import Adam
import os

dataset_path = "paddy images"  # Make sure this folder contains 5 subfolders (categories)
img_size = (128, 128)
batch_size = 32

# Data Preprocessing
datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

train_data = datagen.flow_from_directory(dataset_path, target_size=img_size, batch_size=batch_size, class_mode='categorical', subset='training')
val_data = datagen.flow_from_directory(dataset_path, target_size=img_size, batch_size=batch_size, class_mode='categorical', subset='validation')

num_classes = len(train_data.class_indices)  # Detect number of categories

# CNN Model
cnn_model = Sequential([
    Conv2D(32, (3,3), activation='relu', input_shape=(128,128,3)),
    MaxPooling2D(2,2),
    Flatten(),
    Dense(128, activation='relu'),
    Dense(num_classes, activation='softmax')
])
cnn_model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])
cnn_model.fit(train_data, validation_data=val_data, epochs=2)
cnn_model.save("models/cnn_model.h5")

# ResNet Model
resnet_model = ResNet50(weights=None, input_shape=(128,128,3), classes=num_classes)
resnet_model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])
resnet_model.fit(train_data, validation_data=val_data, epochs=1)
resnet_model.save("models/resnet_model.h5")

# EfficientNet Model
efficient_model = EfficientNetB0(weights=None, input_shape=(128,128,3), classes=num_classes)
efficient_model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])
efficient_model.fit(train_data, validation_data=val_data, epochs=2)
efficient_model.save("models/efficientnet_model.h5")

print("Training complete! Models saved in 'models/' directory.")
