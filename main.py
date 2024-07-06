import os
import google.generativeai as genai
from dotenv import load_dotenv
import tkinter as tk
from tkinter import scrolledtext

# Cargar las variables de entorno
load_dotenv()

API_KEY = os.getenv('GEMINI_API_KEY')

genai.configure(
    api_key=API_KEY
)

model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])
instruction = "En este chat se responde en español: "

# Colores para la interfaz
bg_color = "#2E2E2E"
fg_color = "#FFFFFF"
entry_bg_color = "#3C3C3C"
entry_fg_color = "#FFFFFF"
button_bg_color = "#5C5C5C" 
button_fg_color = "#FFFFFF"

# Colores específicos para el usuario y el bot
user_text_color = "#FFF"
bot_text_color = "#00FFFF"

# Crear la ventana principal
root = tk.Tk()
root.title("Annie")
root.configure(bg=bg_color)
root.geometry("800x600")  # Configuración inicial de tamaño de ventana

# Permitir que la ventana sea redimensionable
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=0)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=0)

# Crear un widget de texto desplazable para mostrar el historial del chat
chat_history = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled', bg=bg_color, fg=fg_color, insertbackground=fg_color)
chat_history.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

# Crear un widget de entrada para la entrada del usuario
user_input = tk.Entry(root, width=80, bg=entry_bg_color, fg=entry_fg_color, insertbackground=entry_fg_color)
user_input.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

# Definir la función para enviar mensajes
def send_message():
    question = user_input.get().strip()
    if question:
        chat_history.config(state='normal')
        chat_history.insert(tk.END, "Tu: " + question + "\n", ("user",))
        chat_history.tag_config("user", foreground=user_text_color)
        chat_history.config(state='disabled')
        user_input.delete(0, tk.END)

        # Enviar el mensaje al chatbot
        full_message = instruction + question
        response = chat.send_message(full_message)

        # Mostrar la respuesta en el historial del chat
        chat_history.config(state='normal')
        chat_history.insert(tk.END, "\nAnnie: " + response.text.strip() + "\n\n", ("bot",))
        chat_history.tag_config("bot", foreground=bot_text_color)
        chat_history.config(state='disabled')

        # Desplazarse automáticamente hasta el final
        chat_history.yview(tk.END)

# Definir la función para limpiar el historial del chat
def clear_chat():
    chat_history.config(state='normal')
    chat_history.delete(1.0, tk.END)
    chat_history.config(state='disabled')

# Crear un botón para enviar el mensaje
send_button = tk.Button(root, text="Enviar", command=send_message, bg=button_bg_color, fg=button_fg_color)
send_button.grid(row=1, column=1, padx=10, pady=10)

# Crear un botón para limpiar el historial del chat
clear_button = tk.Button(root, text="Limpiar", command=clear_chat, bg=button_bg_color, fg=button_fg_color)
clear_button.grid(row=1, column=2, padx=10, pady=10)

# Vincular la tecla Return para enviar el mensaje
root.bind('<Return>', lambda event: send_message())

# Insertar mensaje de bienvenida
chat_history.config(state='normal')
chat_history.insert(tk.END, "Bienvenido al chatbot Annie\n\n", ("bot",))
chat_history.tag_config("bot", foreground=bot_text_color)
chat_history.config(state='disabled')

# Ejecutar el bucle de eventos principal
root.mainloop()
