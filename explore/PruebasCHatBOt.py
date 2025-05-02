from typing import List, Tuple
from utils.chatbot import ChatBot
import os


def chat_with_bot():
    chatbot_history = []  # Historial de la conversación
    test_bot = ChatBot()

    print("¡Hola! Soy el ChatBot. Puedes preguntar sobre productos.")
    print("Escribe 'salir' para terminar la conversación.\n")

    while True:
        message = input("Tú: ")

        if message.lower() == "salir":
            print("¡Adiós! Hasta la próxima.")
            break

        chat_type = "Q&A with stored SQL-DB"
        app_functionality = "Chat"

        # Obtener la respuesta del bot
        response, chatbot_history = test_bot.respond(chatbot_history, message, chat_type, app_functionality)

        print(f"Bot: {response}")

        # Mostrar el historial de la conversación
        print("\nHistorial de la conversación:")
        for msg, resp in chatbot_history:
            print(f"Tú: {msg} -> Bot: {resp}")
        print("\n")


# Ejecutar la función para iniciar la conversación
chat_with_bot()