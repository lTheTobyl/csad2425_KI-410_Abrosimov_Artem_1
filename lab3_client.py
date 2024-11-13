## @file
#  @brief Implementation of a Tic-Tac-Toe game with serial communication and XML configuration.
#  This module sets up a GUI for playing Tic-Tac-Toe using tkinter, communicates with an Arduino
#  via serial port, and uses XML for configuration settings.

import tkinter as tk
from tkinter import messagebox, simpledialog
import serial
import threading
import random
import xml.etree.ElementTree as ET

## @brief Load configuration settings from an XML file.
#  @return Tuple containing port, baud rate, and timeout settings.
def load_config():
    tree = ET.parse('config.xml')
    root = tree.getroot()
    serial_config = root.find('serial')
    port = serial_config.find('port').text
    baud_rate = int(serial_config.find('baudRate').text)
    timeout = int(serial_config.find('timeout').text)
    return port, baud_rate, timeout

port, baud_rate, timeout = load_config()

ser = serial.Serial(port, baud_rate, timeout=timeout)

## @brief Update the game board based on serial input.
#  Continuously reads data from the serial port and updates the GUI accordingly.
def update_board():
    while True:
        data = ser.readline()
        if data:
            data_str = data.decode().strip()
            if "wins" in data_str or "Draw!" in data_str:
                messagebox.showinfo("Game Over", data_str)
                ask_restart()
            else:
                row_data = data_str.split(',')
                if len(row_data) == 9:
                    for i in range(3):
                        for j in range(3):
                            buttons[i][j].config(text=row_data[i*3 + j])

## @brief Prompt for game restart.
#  Asks the user if they want to play again and resets the board or closes the application.
def ask_restart():
    if messagebox.askyesno("Restart", "Do you want to play again?"):
        ser.write(b'r')  # Send restart command to Arduino
        reset_board()
        root.after(100, select_game_mode)
    else:
        root.destroy()

## @brief Reset the game board to initial state.
#  Resets all buttons on the game board to their initial state.
def reset_board():
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text=str(i*3 + j + 1), state=tk.NORMAL)

## @brief Handle button click events.
#  Processes a button click, updates the game state, and initiates computer move if necessary.
#  @param id Button id.
#  @param from_computer Indicates if the move is made by the computer.
def button_click(id, from_computer=False):
    if buttons[(id - 1) // 3][(id - 1) % 3]['state'] == tk.DISABLED:
        return
    ser.write(str(id).encode())
    buttons[(id - 1) // 3][(id - 1) % 3].config(text='X' if game_mode == 'singleO' else 'O', state=tk.DISABLED)
    if not from_computer and game_mode != "multi":
        computer_move()

## @brief Make a computer move.
#  Chooses a random available button for the computer's move.
def computer_move():
    available = [i * 3 + j + 1 for i in range(3) for j in range(3) if buttons[i][j]['state'] != tk.DISABLED]
    if available:
        move = random.choice(available)
        button_click(move, from_computer=True)

## @brief Select the game mode via a dialog.
#  Asks the user to choose between single player or multiplayer modes.
def select_game_mode():
    global game_mode
    game_mode = simpledialog.askstring("Game Mode", "Enter game mode: 'singleX', 'singleO', or 'multi'")
    if game_mode and game_mode.startswith('single'):
        computer_symbol = 'X' if game_mode == 'singleO' else 'O'
        player_symbol = 'O' if game_mode == 'singleO' else 'X'
        messagebox.showinfo("Game Mode", f"You are '{player_symbol}'. Computer is '{computer_symbol}'.")
        if game_mode == 'singleO':
            computer_move()

root = tk.Tk()
root.title("Tic-Tac-Toe")

buttons = [[None]*3 for _ in range(3)]
for i in range(3):
    for j in range(3):
        id = 3 * i + j + 1
        button = tk.Button(root, text=str(id), width=10, height=3, command=lambda id=id: button_click(id))
        button.grid(row=i, column=j)
        buttons[i][j] = button

select_game_mode()
thread = threading.Thread(target=update_board)
thread.daemon = True
thread.start()

root.mainloop()
