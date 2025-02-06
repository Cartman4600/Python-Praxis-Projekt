import tkinter as tk    # Gui graphical user interface
from tkinter import ttk

# Real Estate Price Calculator REPC
window = tk.Tk()                                # Erstellt ein GUI Fenstser
window.geometry("800x600")                      # Legt die Größe des Fensters fest
window.title("Real Estate Price Calculator")    # Gibt dem Fenster einen Titel


my_label = tk.Label(window, text='Willkommen!').grid(row=0, column=4)                               # Erstellt ein Label im Fenster "window"

label_checkbuttons = tk.Label(window, text ="Ausstattung:").grid(row=0, sticky=tk.W)

var1 = tk.IntVar()                                                                                  # Erstellt Checkbuttons und verknüft mit Variablen
tk.Checkbutton(window, text='Zentralheizung', variable=var1).grid(row=1, sticky=tk.W)               # varx.get() gibt den Wert der Checkbox zurück         
var2 = tk.IntVar()                                                                                  # 1 für checked, 0 für unchecked
tk.Checkbutton(window, text='Fußbodenheizung', variable=var2).grid(row=2, sticky=tk.W)
var3 = tk.IntVar()
tk.Checkbutton(window, text='Dachboden', variable=var3).grid(row=1, column=1, sticky=tk.W)
var4 = tk.IntVar()
tk.Checkbutton(window, text='Keller', variable=var4).grid(row=2, column=1 , sticky=tk.W)

tk.Label(window, text='Wie viel m² Grundstück').grid(row=3)                                         # Erstell Entry für Nutzereingaben
tk.Label(window, text='Wie viel m² Wohnfläche').grid(row=4)
e1 = tk.Entry(window)                                                                               # e1.get() gibt den Wert des Entry zurück
e2 = tk.Entry(window)                                                                               # Button basteln um sie per funktion zu speichern.
e1.grid(row=3, column=1)
e2.grid(row=4, column=1)

label_radiobuttons = tk.Label(window, text ="Gegend:").grid(row=5, sticky=tk.W)                     # Erstellt Radiobuttons und verknüpft sie mit einer Variablen
radiobutton_var = tk.IntVar()
tk.Radiobutton(window, text='Stadt', variable=radiobutton_var, value=1).grid(row=6)
tk.Radiobutton(window, text='Land', variable=radiobutton_var, value=2).grid(row=7)

label_listbox = tk.Label(window, text ="Bundesland:").grid(row=8, sticky=tk.W)

bundesland_listbox = tk.Listbox(window) 
bundesland_listbox.grid(row=9)                                                                      # Erstellt Listbox
bundeslaender = [
    "Baden-Württemberg",
    "Bayern",
    "Berlin",
    "Brandenburg",
    "Bremen",
    "Hamburg",
    "Hessen",
    "Mecklenburg-Vorpommern",
    "Niedersachsen",
    "Nordrhein-Westfalen",
    "Rheinland-Pfalz",
    "Saarland",
    "Sachsen",
    "Sachsen-Anhalt",
    "Schleswig-Holstein",
    "Thüringen"
]
for bundesland in bundeslaender:
    bundesland_listbox.insert(bundeslaender.index(bundesland)+1, bundesland)                        # Fügt Bundesländer zu Listbox hinzu


label_combobox = tk.Label(window, text="Bundesland auswählen:")                                     # Label für Combobox
label_combobox.grid(row=10, sticky=tk.W)

def select(event):                                                                                  # Wenn eine Bundesland ausgewählt wird, wird es gespeichert
    global combobox_item 
    combobox_item = combo_box.get()                                                                 # Speichert den momentan ausgewählten Combobox Inhalt.

combo_box = ttk.Combobox(window, values=bundeslaender)
combo_box.grid(row=11, sticky=tk.W)
combo_box.set("Bundesland")                                                                         # Defaul Wert der Combobox
combo_box.bind("<<ComboboxSelected>>", select)                                                      # Event Handle, wird etwas ausgewählt, wird select funktion ausgeführt

button = tk.Button(window, text='Exit', width=25, command=window.destroy).grid(row=12, sticky=tk.W) # Erstellt Button mit der exit Funktion


window.mainloop()                                                                                   # Startet das GUI