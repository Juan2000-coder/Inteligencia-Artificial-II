import subprocess
try:
    import tensorflow as tf
except ImportError as err:
    subprocess.check_call(['pip', 'install', 'tensorflow'])
    subprocess.check_call(['pip', 'install', 'Pillow'])
    import tensorflow as tf

from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
from tensorflow.keras.callbacks import EarlyStopping
import os
import random
import numpy as np
import matplotlib.pyplot as plt

# Función para visualizar los filtros de una capa convolucional
def visualize_filters(model, layer_name):
    # Obtener la capa convolucional por nombre
    layer = model.get_layer(name=layer_name)
    
    # Obtener los pesos de la capa
    filters, biases = layer.get_weights()
    
    # Normalizar los filtros para visualización
    f_min, f_max = filters.min(), filters.max()
    filters = (filters - f_min) / (f_max - f_min)
    
    # Número de filtros
    n_filters = filters.shape[3]
    
    # Número de filas y columnas para la visualización
    n_columns = 8
    n_rows = int(np.ceil(n_filters / n_columns))
    
    # Crear una figura para los filtros
    fig, axes = plt.subplots(n_rows, n_columns, figsize=(n_columns, n_rows))
    
    for i in range(n_filters):
        # Obtener el filtro i-ésimo
        f = filters[:, :, 0, i]
        
        # Ejes para el filtro i-ésimo
        ax = axes[i // n_columns, i % n_columns]
        
        # Visualizar el filtro
        ax.imshow(f, cmap='gray')
        ax.axis('off')
    
    # Quitar los ejes para filtros vacíos
    for j in range(i + 1, n_rows * n_columns):
        axes[j // n_columns, j % n_columns].axis('off')
    plt.show()


# Rutas de las carpetas
source_dir = "images"

train_dir = source_dir + "/train/"
test_dir = source_dir + "/test/"

# Clases (nombres de las subcarpetas)
classes = ["up", "down", "right"]

# Crea los directorios de entrenamiento y prueba si no existen
os.makedirs(train_dir, exist_ok=True)
os.makedirs(test_dir, exist_ok=True)

# Crea los directorios de entrenamiento y prueba si no existen
os.makedirs(train_dir + classes[0], exist_ok=True)
os.makedirs(train_dir + classes[1], exist_ok=True)
os.makedirs(train_dir + classes[2], exist_ok=True)

# Proporción de imágenes para entrenamiento y prueba
train_ratio = 1


image_size = (128, 128)
input_shape = image_size + (1,)  # Tamaño de la imagen con un solo canal para escala de grises

# Función para cargar imágenes y convertirlas a escala de grises
def load_and_preprocess_image(file_path, target_size):
    img = load_img(file_path, color_mode='grayscale', target_size=target_size)
    img_array = img_to_array(img)
    return img_array / 255.0  # Normaliza los valores de píxeles entre 0 y 1

# Iterar sobre las subcarpetas
for class_name in classes:
    # Ruta de la subcarpeta de origen
    source_class_dir = os.path.join(source_dir, class_name)
    
    # Obtener la lista de imágenes en la subcarpeta de origen
    images = os.listdir(source_class_dir)
    
    # Mezclar aleatoriamente las imágenes
    random.shuffle(images)
    
    # Calcular el número de imágenes para entrenamiento
    num_train_images = int(len(images) * train_ratio)
    
    # Iterar sobre las imágenes para entrenamiento
    for img_name in images[:num_train_images]:
        # Ruta de la imagen de origen
        src_img_path = os.path.join(source_class_dir, img_name)
        # Ruta de destino para la imagen de entrenamiento
        dest_train_path = os.path.join(train_dir + class_name, f"{img_name}")
        # Mover la imagen a la carpeta de entrenamiento y renombrarla
        img_array = load_and_preprocess_image(src_img_path, image_size)
        tf.keras.preprocessing.image.save_img(dest_train_path, img_array)
    
    # Iterar sobre las imágenes para prueba
    for img_name in images[num_train_images:]:
        # Ruta de la imagen de origen
        src_img_path = os.path.join(source_class_dir, img_name)
        # Ruta de destino para la imagen de prueba
        dest_test_path = os.path.join(test_dir + class_name, f"{img_name}")
        # Mover la imagen a la carpeta de prueba y renombrarla
        img_array = load_and_preprocess_image(src_img_path, image_size)
        tf.keras.preprocessing.image.save_img(dest_train_path, img_array)


# Parámetros para el modelo
batch_size = 16

# Crear generadores de datos
train_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=image_size,
    batch_size=batch_size,
    class_mode='categorical',
    color_mode='grayscale')  # Se especifica el modo de color escala de grises

validation_datagen = ImageDataGenerator(rescale=1./255)
validation_generator = validation_datagen.flow_from_directory(
    test_dir,
    target_size=image_size,
    batch_size=batch_size,
    class_mode='categorical',
    color_mode='grayscale')  # Se especifica el modo de color escala de grises


data_aux = 3
# ========================== Construir el modelo ==========================================
model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (data_aux, data_aux), activation='relu', input_shape=input_shape, name = 'conv1'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(64, (data_aux, data_aux), activation='relu', name = 'conv2'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(128, (data_aux, data_aux), activation='relu', name = 'conv3'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(len(classes), activation='softmax')
])
# ==========================================================================================

# Compilar el modelo
#model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.00001, decay=1e-6),loss='categorical_crossentropy', metrics=['accuracy'])
model.compile(optimizer= tf.keras.optimizers.Adam(learning_rate=0.00001),loss='categorical_crossentropy', metrics=['accuracy'])
print("Número total de muestras de entrenamiento:", train_generator.samples)
print("Número total de muestras de validación:", validation_generator.samples)
# Callbacks
es = tf.keras.callbacks.EarlyStopping(min_delta=0.00005, patience=10, verbose=1, restore_best_weights=True)
#es = EarlyStopping(monitor='loss', baseline=0.0001, patience=10, restore_best_weights=True)
rlr = tf.keras.callbacks.ReduceLROnPlateau(factor=0.5, patience=3, min_lr=1e-10, verbose=1)

# Entrenar el modelo
model.fit(train_generator, epochs=100, callbacks=[es,rlr], verbose=1, validation_data=validation_generator)

# Visualizacion de filtros
visualize_filters(model, 'conv1')
visualize_filters(model, 'conv2')
visualize_filters(model, 'conv3')

# Guardar el modelo
model.save('tensorflow_nn.h5')