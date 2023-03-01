#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 00:38:21 2023

@author: Jason
"""

import os
import tkinter as tk
from elo_system5 import EloSystem

setValues = []
mode = 0 #0 means default mode, 1 means run_game mode, 2 means set_elo mode
elo = EloSystem()


def get_entry():
    print("mode: " + str(mode))
    if(mode == 2 and len(setValues) != 2):
        
            
        setValues.append(entry.get())
        entry.delete(0, "end")
        entryLabel['text'] = "What ELO?"
    elif (mode == 2 and len(setValues) == 2):
        print("cheese")
        print(str(setValues[0]), str(setValues[1]))
        elo.set_elo((setValues[0]), setValues[1])
        setValues.clear()
        #show_ratings()
    elif (mode == 0):
        print("default mode")
    elif (mode == 1):
        print("mode is 1")
    else:
        entryLabel['text'] = "Press set_gui button to finish"
    
    print(setValues)

def set_eloGUI():
    global mode
    mode = 2
    setValues.clear()
    print("button clicked")
    
    
    
    
    entryLabel['text'] = "Which Player?"
   
    print(setValues)
    #EloSystem().set_elo(player, rating)

def run():
    
    os.system('python3 run_game.py')



def test_function(entry):
    print("this is the entry:", entry)
    
    #return EloSystem().print_ratings()
    
    
    
#show ratings 
def show_ratings():
    
    rating_output = elo.print_ratings()
    consoleLabel['text'] = rating_output




HEIGHT = 700
WIDTH = 800

#window
root = tk.Tk()

#canvas in window
canvas = tk.Canvas(root, height=HEIGHT, width = WIDTH)
canvas.pack()

#background image
background_image = tk.PhotoImage(file= 'ocean.png')
background_label = tk.Label(root, image = background_image)
background_label.place(relwidth = 1, relheight = 1)



#frame.place(relx = 0.1, rely = 0.1, relwidth = 0.8, relheight = 0.8)

consoleFrame = tk.Frame(root, bg = 'red')
consoleFrame.place(relx = 0.15, rely = 0.2, relwidth = 0.4, relheight = 0.45)

#frame in canvas
consoleLabel = tk.Label(root)
consoleLabel.place(relx = 0.15, rely = 0.2, relwidth = 0.45, relheight = 0.45)
#consoleLabel['text'] = lambda: show_ratings


    


#button
runButton = tk.Button(root, text = "Run Game", fg = 'red', command= run)
runButton.place(relx = 0.7, rely = 0.2, relwidth = 0.2, relheight = 0.05)


setEloButton = tk.Button(root, text = "Set Elo", command = set_eloGUI)
setEloButton.place(relx = 0.7, rely = 0.3, relwidth = 0.2, relheight = 0.05)

showRatingsButton = tk.Button(root, text = "Show Ratings", command = show_ratings)
showRatingsButton.place(relx = 0.7, rely = 0.4, relwidth = 0.2, relheight = 0.05)

enterButton = tk.Button(root, text = "Enter", command = get_entry)
enterButton.place(relx = 0.6, rely = 0.85, relwidth = 0.2, relheight = 0.05)

#label
label = tk.Label(root, text = "This is Pong")
label.place(relx = 0.3, rely = 0.05, relwidth = 0.4, relheight= 0.1)

entryLabel = tk.Label(root, bg = 'white', borderwidth = 0.15, text = "Choose a Button", fg = 'black')
entryLabel.place(relx = 0.15, rely = 0.75, relwidth = 0.3,  relheight = 0.05)

#input entry
entry = tk.Entry(root, bg = 'green')
entry.place(relx = 0.15, rely = 0.85, relwidth = 0.4, relheight = 0.05)

#runs gui
root.mainloop()