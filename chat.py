import pickle
import json
import random
import nltk
from nltk.stem import WordNetLemmatizer

# Inicializar lematizador
lemmatizer = WordNetLemmatizer()

# Cargar el modelo guardado y los datos de intenciones
with open('chatbot_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('intents.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

def get_response(user_input):
    # Preprocesar la entrada del usuario
    user_input = user_input.lower()
    words = nltk.word_tokenize(user_input)
    words = [lemmatizer.lemmatize(w) for w in words]
    processed_input = " ".join(words)

    # Predecir la intención
    prediction = model.predict([processed_input])

    # Obtener la probabilidad de la predicción
    probabilities = model.predict_proba([processed_input])
    max_prob = max(probabilities[0])

    # Umbral de confianza: si es menor a 0.7, consideramos que no entendió.
    if max_prob < 0.4:
        tag = "sin_respuesta"
    else:
        tag = prediction[0]

    # Seleccionar una respuesta aleatoria
    for intent in data['intents']:
        if intent['tag'] == tag:
            response = random.choice(intent['responses'])
            return response

    return "Lo siento, algo salió mal."

# Bucle principal para chatear
print("¡Hola! Soy tu chatbot. Escribe 'salir' para terminar.")
while True:
    user_message = input("Tú: ")
    if user_message.lower() == 'salir':
        break

    bot_response = get_response(user_message)
    print(f"Bot: {bot_response}")