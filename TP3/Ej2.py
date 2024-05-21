from sklearn.experimental import enable_hist_gradient_boosting
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.cluster import KMeans
from keras.datasets import mnist
import matplotlib.pyplot as plt
from sklearn.svm import SVC
import numpy as np


#-------------------------------------------- Preprocesado --------------------------------------------#
# Cargar el dataset MNIST
(X_train, y_train), (X_test, y_test) = mnist.load_data()

# Normalización de las imágenes
X_train = X_train.reshape(X_train.shape[0], -1) / 255.0
X_test = X_test.reshape(X_test.shape[0], -1) / 255.0

print("X_train shape:", X_train.shape)
print("y_train shape:", y_train.shape)
print("X_test shape:", X_test.shape)
print("y_test shape:", y_test.shape)


# Dividir los datos en conjuntos de entrenamiento y prueba
X_train_split, X_val_split, y_train_split, y_val_split = train_test_split(X_train, y_train, test_size=0.2, random_state=42)


#------------------------------------------- Clasificacion --------------------------------------------#
# Clasificador K-Nearest Neighbors (KNN)
knn_clf = KNeighborsClassifier(n_neighbors=3)
knn_clf.fit(X_train_split, y_train_split)
y_pred_knn = knn_clf.predict(X_val_split)
accuracy_knn = accuracy_score(y_val_split, y_pred_knn)
print("Precisión del modelo KNN:", accuracy_knn)

# Clasificador K-Means
kmeans = KMeans(n_clusters=10, n_init=10, random_state=42)
kmeans.fit(X_train)
y_pred_kmeans = kmeans.predict(X_val_split)
labels_map = {}
for cluster in range(10):
    labels = y_val_split[y_pred_kmeans == cluster]
    most_common_label = np.argmax(np.bincount(labels))
    labels_map[cluster] = most_common_label
y_pred_kmeans_mapped = [labels_map[cluster] for cluster in y_pred_kmeans]
accuracy_kmeans = accuracy_score(y_val_split, y_pred_kmeans_mapped)
print("Precisión del modelo K-Means:", accuracy_kmeans)

# Clasificador Support Vector Machine (SVM)
svm_clf = SVC(kernel='rbf', gamma='scale', random_state=42)
svm_clf.fit(X_train_split, y_train_split)
y_pred_svm = svm_clf.predict(X_val_split)
accuracy_svm = accuracy_score(y_val_split, y_pred_svm)
print("Precisión del modelo SVM:", accuracy_svm)

# Clasificador Random Forest
rf_clf = RandomForestClassifier(n_estimators=100, random_state=42)
rf_clf.fit(X_train_split, y_train_split)
y_pred_rf = rf_clf.predict(X_val_split)
accuracy_rf = accuracy_score(y_val_split, y_pred_rf)
print("Precisión del modelo Random Forest:", accuracy_rf)

# Clasificador Naive Bayes Gaussiano
nb_clf = GaussianNB()
nb_clf.fit(X_train_split, y_train_split)
y_pred_nb = nb_clf.predict(X_val_split)
accuracy_nb = accuracy_score(y_val_split, y_pred_nb)
print("Precisión del modelo Naive Bayes Gaussiano:", accuracy_nb)

# Clasificador Gradient Boosting
'''gb_clf = GradientBoostingClassifier(n_estimators=100, random_state=42)
gb_clf.fit(X_train_split, y_train_split)
y_pred_gb = gb_clf.predict(X_val_split)
accuracy_gb = accuracy_score(y_val_split, y_pred_gb)
print("Precisión del modelo Gradient Boosting:", accuracy_gb)'''

# Clasificador HistGradientBoosting    (Versión de Gradient Boosting optimizada para datasets grandes n>=10000)
hgb_clf = HistGradientBoostingClassifier(random_state=42)       
hgb_clf.fit(X_train_split, y_train_split)
y_pred_hgb = hgb_clf.predict(X_val_split)
accuracy_hgb = accuracy_score(y_val_split, y_pred_hgb)
print("Precisión del modelo HistGradientBoosting:", accuracy_hgb)


#------------------------ Matrices de confusion para verificar los resultados -------------------------#
# Calcular las matrices de confusión
cm_knn = confusion_matrix(y_val_split, y_pred_knn)
cm_kmeans = confusion_matrix(y_val_split, y_pred_kmeans_mapped)
cm_svm = confusion_matrix(y_val_split, y_pred_svm)
cm_rf = confusion_matrix(y_val_split, y_pred_rf)
cm_nb = confusion_matrix(y_val_split, y_pred_nb)
#cm_gb = confusion_matrix(y_val_split, y_pred_gb)
cm_hgb = confusion_matrix(y_val_split, y_pred_hgb)

# Graficar las matrices de confusión
classes = np.arange(10)
plt.figure(figsize=(20, 10))

plt.subplot(2, 3, 1)
plt.imshow(cm_knn, interpolation='nearest', cmap=plt.cm.Blues)
plt.title('Matriz de Confusión - KNN')
plt.colorbar()
plt.xticks(classes, classes)
plt.yticks(classes, classes)
plt.xlabel('Etiqueta Predicha')
plt.ylabel('Etiqueta Verdadera')

plt.subplot(2, 3, 2)
plt.imshow(cm_kmeans, interpolation='nearest', cmap=plt.cm.Blues)
plt.title('Matriz de Confusión - K-Means')
plt.colorbar()
plt.xticks(classes, classes)
plt.yticks(classes, classes)
plt.xlabel('Etiqueta Predicha')
plt.ylabel('Etiqueta Verdadera')

plt.subplot(2, 3, 3)
plt.imshow(cm_svm, interpolation='nearest', cmap=plt.cm.Blues)
plt.title('Matriz de Confusión - SVM')
plt.colorbar()
plt.xticks(classes, classes)
plt.yticks(classes, classes)
plt.xlabel('Etiqueta Predicha')
plt.ylabel('Etiqueta Verdadera')

plt.subplot(2, 3, 4)
plt.imshow(cm_rf, interpolation='nearest', cmap=plt.cm.Blues)
plt.title('Matriz de Confusión - Random Forest')
plt.colorbar()
plt.xticks(classes, classes)
plt.yticks(classes, classes)
plt.xlabel('Etiqueta Predicha')
plt.ylabel('Etiqueta Verdadera')

plt.subplot(2, 3, 5)
plt.imshow(cm_nb, interpolation='nearest', cmap=plt.cm.Blues)
plt.title('Matriz de Confusión - Naive Bayes Gaussiano')
plt.colorbar()
plt.xticks(classes, classes)
plt.yticks(classes, classes)
plt.xlabel('Etiqueta Predicha')
plt.ylabel('Etiqueta Verdadera')

'''plt.subplot(2, 3, 6)
plt.imshow(cm_gb, interpolation='nearest', cmap=plt.cm.Blues)
plt.title('Matriz de Confusión - Gradient Boosting')
plt.colorbar()
plt.xticks(classes, classes)
plt.yticks(classes, classes)
plt.xlabel('Etiqueta Predicha')
plt.ylabel('Etiqueta Verdadera')'''

plt.subplot(2, 3, 6)
plt.imshow(cm_hgb, interpolation='nearest', cmap=plt.cm.Blues)
plt.title('Matriz de Confusión - Hist Gradient Boosting')
plt.colorbar()
plt.xticks(classes, classes)
plt.yticks(classes, classes)
plt.xlabel('Etiqueta Predicha')
plt.ylabel('Etiqueta Verdadera')

plt.tight_layout()
plt.show()



'''
# Mostrar 15 ejemplos aleatorios
r, c = 3, 5
fig = plt.figure(figsize=(2*c, 2*r))
for _r in range(r):
    for _c in range(c):
        ix = np.random.randint(0, len(X_train))
        img = X_train[ix]
        plt.subplot(r, c, _r*c + _c + 1)
        plt.imshow(img, cmap='gray')
        plt.axis("off")
        plt.title(y_train[ix])
plt.tight_layout()
plt.show()
'''