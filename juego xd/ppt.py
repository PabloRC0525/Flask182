import tkinter as tk
import random

def determine_winner(player_choice, computer_choice):
    if player_choice == computer_choice:
        return "Empate"
    elif (player_choice == "Piedra" and computer_choice == "Tijeras") or \
         (player_choice == "Papel" and computer_choice == "Piedra") or \
         (player_choice == "Tijeras" and computer_choice == "Papel"):
        return "¡Ganaste!"
    else:
        return "¡Perdiste!"

def play_game(player_choice):
    choices = ["Piedra", "Papel", "Tijeras"]
    computer_choice = random.choice(choices)
    result = determine_winner(player_choice, computer_choice)
    result_label.config(text=f"Elegiste: {player_choice}\n"
                             f"La computadora eligió: {computer_choice}\n"
                             f"{result}")

# Configuración de la ventana
window = tk.Tk()
window.title("Piedra, Papel, Tijeras")

# Etiqueta de título
title_label = tk.Label(window, text="¡Piedra, Papel, Tijeras!")
title_label.pack(pady=10)

# Botones para las elecciones del jugador
rock_button = tk.Button(window, text="Piedra", command=lambda: play_game("Piedra"))
paper_button = tk.Button(window, text="Papel", command=lambda: play_game("Papel"))
scissors_button = tk.Button(window, text="Tijeras", command=lambda: play_game("Tijeras"))

rock_button.pack(padx=20, pady=5)
paper_button.pack(padx=20, pady=5)
scissors_button.pack(padx=20, pady=5)

# Etiqueta para mostrar el resultado
result_label = tk.Label(window, text="")
result_label.pack(pady=10)

# Iniciar la aplicación
window.mainloop()
