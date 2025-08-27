import json
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import pickle

# Inicializar lematizador
lemmatizer = WordNetLemmatizer()

# Cargar el archivo de intenciones
with open('intents.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Preprocesamiento de los datos
training_sentences = []
training_labels = []
labels = []

for intent in data['intents']:
    for pattern in intent['patterns']:
        # Tokenizar y lematizar cada palabra en la oración
        words = nltk.word_tokenize(pattern)
        words = [lemmatizer.lemmatize(w.lower()) for w in words]
        training_sentences.append(" ".join(words))
        training_labels.append(intent['tag'])

    # Guardar la etiqueta si no está ya en la lista
    if intent['tag'] not in labels:
        labels.append(intent['tag'])

# Crear y entrenar el modelo de Machine Learning
# Usaremos un pipeline para simplificar: TfidfVectorizer + Naive Bayes
model = make_pipeline(TfidfVectorizer(ngram_range=(1,2)), MultinomialNB())
model.fit(training_sentences, training_labels)

# Guardar el modelo entrenado
with open('chatbot_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("¡Modelo entrenado y guardado exitosamente!")