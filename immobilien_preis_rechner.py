from reportlab.pdfgen import canvas                # erstellt pdfs
from reportlab.pdfbase.ttfonts import TTFont       # Fonts
from reportlab.pdfbase import pdfmetrics           
from reportlab.lib import colors                   # Farben
import pandas as pd                                # pandas kann Excel Dateien lesen
import tkinter as tk                               # Gui graphical user interface
from tkinter import  ttk                           # ttk muss explizit extra importiert werden
from tkinter import messagebox                     # Pop Up Fehler Fenster
import datetime as dt                              # Für das aktuelle Jahr
import os                                          # Filemanagment
import pygame                                      # Library Spiele, wir nutzen nur die Tonausgabe

##################################################################################################

# Standardwerte für Kostenfaktoren
bundeslaender_standard_dict = {  "Baden-Württemberg": 1.5,
                                 "Bayern": 1.7,
                                 "Berlin": 2.1,
                                 "Brandenburg": 1.1,
                                 "Bremen": 1.2,
                                 "Hamburg": 2.5,
                                 "Hessen": 1.3,
                                 "Mecklenburg-Vorpommern": 0.9,
                                 "Niedersachsen": 1.0,
                                 "Nordrhein-Westfalen": 1.1,
                                 "Rheinland-Pfalz": 1.0,
                                 "Saarland": 0.7,
                                 "Sachsen": 0.7,
                                 "Sachsen-Anhalt": 0.6,
                                 "Schleswig-Holstein": 1.4,
                                 "Thüringen": 0.6
                              }

region_standard_dict = {"Land": 1,
                        "Stadt": 2
                        }

ausstattung_standard_dict = { "Rohbau": 0.5,
                              "Sanierungsbedarf": 0.8,
                              "Renovierungsbedarf": 0.9,
                              "Einfach": 1.0,
                              "Gehoben": 2.0
                            }

hausart_standard_dict = {"Einfamilienhaus": 1,
                        "Doppelhaushälfte": 0.8,
                        "Mehrfamilienhaus": 0.7
                        }

grundstueck_standard_preis = 160
wohnflaeche_standard_preis = 2500

architekt_standard_rate = 0.2
makler_standard_rate = 0.02
denkmalschutz_standard_rate = 0.20

baujahr_standard_rate = 0.001

selected_bundesland = None                                                                         # Werte auf None um später zu prüfen, ob etwas ausgewählt wurde.
selected_region = None
selected_ausstattung = None
selected_hausart = None

####################################################################################################

class Immobilie:
   
   
   def __init__(self,
                bundeslaender_dict:dict = bundeslaender_standard_dict,                             # Standardwerte von oben, falls nichts angegeben wird
                region_dict:dict = region_standard_dict,
                ausstattung_dict:dict = ausstattung_standard_dict,
                hausart_dict:dict = hausart_standard_dict,
                grundstueck_preis:int = grundstueck_standard_preis,
                wohnflaeche_preis:int = wohnflaeche_standard_preis,
                architekt_rate:float = architekt_standard_rate,
                makler_rate:float = makler_standard_rate,
                denkmalschutz_rate:float = denkmalschutz_standard_rate,
                baujahr_rate:float = baujahr_standard_rate,
                grundstuecksflaeche:int = 0,
                wohnflaeche:int = 0,
                baujahr:int = 1900
                ) -> None:
      
      self.bundeslaender_dict = bundeslaender_dict
      self.region_dict = region_dict
      self.ausstattung_dict = ausstattung_dict
      self.hausart_dict = hausart_dict
      self.grundstueck_preis = grundstueck_preis
      self.wohnflaeche_preis = wohnflaeche_preis
      self.architekt_rate = architekt_rate
      self.makler_rate = makler_rate
      self.denkmalschutz_rate = denkmalschutz_rate
      self.baujahr_rate = baujahr_rate
      self.grundstuecksflaeche = grundstuecksflaeche
      self.wohnflaeche = wohnflaeche
      self.baujahr = baujahr


   def grundpreis(self) -> int:

      result_grundstueck = (self.grundstuecksflaeche - self.wohnflaeche) * self.grundstueck_preis
      result_wohnflaeche = self.wohnflaeche * self.wohnflaeche_preis
      result = result_grundstueck + result_wohnflaeche
      return result


   def baujahr_faktor(self) -> float:
      result = 1 - (dt.date.today().year - self.baujahr) * self.baujahr_rate                       # Berechne Baujahr-faktor
      return result


   def berechnung(self, 
                  selected_bundesland:str,
                  selected_region:str, 
                  selected_ausstattung:str, 
                  selected_hausart:str, 
                  architekt_status:int,                                                            # Status int, 0 oder 1
                  markler_status:int, 
                  denkmalschutz_status:int
                  ) -> float:
      
      result = round(self.bundeslaender_dict[selected_bundesland] *                                # Bundesland-faktor
                     self.region_dict[selected_region] *                                           # Region-faktor
                     self.ausstattung_dict[selected_ausstattung] *                                 # Ausstattungs-faktor
                     self.hausart_dict[selected_hausart] *                                         # Hausart-faktor
                     self.baujahr_faktor() *                                                       # Berechne Baujahr-faktor
                     (1 + int(architekt_status) * self.architekt_rate) *                           # Architekt-faktor
                     (1 + int(markler_status) * self.makler_rate) *                                # Markler-faktor
                     (1 + int(denkmalschutz_status) * self.denkmalschutz_rate)*                    # Denkmalschutz-faktor
                     self.grundpreis(),                                                            # Berechne Grundpreis
                     2)                                                                            # Rundungsstellen
      return result
####################################################################################################

# Fenster erstellen

# Real Estate Price Calculator REPC
window = tk.Tk()                                                                                   # Erstellt ein GUI Fenstser
window.geometry("800x600")                                                                         # Legt die Größe des Fensters fest
window.title("Real Estate Price Calculator")                                                       # Gibt dem Fenster einen Titel

# Menubar erstellen
menubar = tk.Menu(window)                                                                          # Erstellt eine Menubar für das Fenster window
filemenu = tk.Menu(menubar, tearoff=0)                                                             # Dropdown Menu, dass nicht abgetrennt(tearoff=0) ist

# Menubar Funktionen
def donothing():
   pass

# Menubar 
filemenu.add_command(label="Preisinfomationen laden", command=donothing)
filemenu.add_separator()
filemenu.add_command(label="Beenden", command=window.destroy)
menubar.add_cascade(label="File", menu=filemenu)

helpmenu = tk.Menu(menubar, tearoff=0)
helpmenu.add_command(label="About", command=donothing)
menubar.add_cascade(label="Help", menu=helpmenu)


####################################################################################################
# Fenster Design

label_welcome = tk.Label(window, text='Willkommen!')                                               # Erstellt ein Label im Fenster "window"
label_welcome.grid(row=0, column=4, sticky=tk.W)   

# Comboboxen Auswahl Funktion
def select_combobox(event, combobox_name:str) -> None:                                             # Wenn eine Bundesland ausgewählt wird, wird es gespeichert
   global selected_bundesland, selected_region
   global selected_ausstattung, selected_hausart

   if combobox_name == "bundesland":
      selected_bundesland = event.widget.get()                                                     # Speichert den momentan ausgewählten Combobox Inhalt als globale variable
   elif combobox_name =="region":                                                                  # In event ist der Wert und welches Widget den Wert beinhaltet gespeichert
      selected_region = event.widget.get()                                                         # mit event.widget.get bekommt man den jeweiligen Wert der zugehörigen Combobox
   elif combobox_name == "ausstattung":
      selected_ausstattung = event.widget.get() 
   elif combobox_name == "hausart":
      selected_hausart = event.widget.get()

# Combobox Bundesländer                                                          
bundeslaender = list(bundeslaender_standard_dict.keys())                                           # Liste der Bundesländer aus dem Dictionary bundeslaender_standard
                  
label_combobox_bundesland = tk.Label(window, text="Bundesland auswählen:")                         # Label für Combobox
label_combobox_bundesland.grid(row=1, column=0, sticky=tk.W)   

combobox_bundesland = ttk.Combobox(window, values=bundeslaender, state="readonly")
combobox_bundesland.grid(row=1, column=1, sticky=tk.W)
combobox_bundesland.set("Bundesland")                                                                 # Defaul Wert der Combobox
combobox_bundesland.bind("<<ComboboxSelected>>", lambda event: select_combobox(event, "bundesland"))  # Event Handle, wird etwas ausgewählt, wird select funktion ausgeführt


# Combobox Region
regionen = list(region_standard_dict.keys())                                                       # Liste der Regionen aus dem Dictionary region_standard
                  
label_combobox_region = tk.Label(window, text="Region auswählen:")                                 # Label für Combobox
label_combobox_region.grid(row=2, sticky=tk.W)

combobox_region = ttk.Combobox(window, values=regionen, state="readonly")
combobox_region.grid(row=2, column=1, sticky=tk.W)
combobox_region.set("Region")                                                                      # Defaul Wert der Combobox
combobox_region.bind("<<ComboboxSelected>>", lambda event: select_combobox(event, "region"))                                        # Event Handle: wird etwas ausgewählt, wird die jeweilige select funktion ausgeführt


# Combobox Ausstatttung
austattungen = list(ausstattung_standard_dict.keys())                                              # Liste der Regionen aus dem Dictionary ausstattungen_standard
                  
label_combobox_ausstattung = tk.Label(window, text="Ausstattung auswählen:")                       # Label für Combobox
label_combobox_ausstattung.grid(row=3, sticky=tk.W)

combobox_ausstattung = ttk.Combobox(window, values=austattungen, state="readonly")
combobox_ausstattung.grid(row=3, column=1,  sticky=tk.W)
combobox_ausstattung.set("Ausstattung")                                                                  # Defaul Wert der Combobox
combobox_ausstattung.bind("<<ComboboxSelected>>", lambda event: select_combobox(event, "ausstattung"))   # Event Handle, wird etwas ausgewählt, wird select funktion ausgeführt


# Combobox Hausart
hausart = list(hausart_standard_dict.keys())                                                       # Liste der Regionen aus dem Dictionary hausart_standard
                  
label_combobox_hausart = tk.Label(window, text="Hausart auswählen:")                               # Label für Combobox
label_combobox_hausart.grid(row=4, sticky=tk.W)

combobox_hausart = ttk.Combobox(window, values=hausart, state="readonly")
combobox_hausart.grid(row=4, column=1, sticky=tk.W)
combobox_hausart.set("Hausart")                                                                    # Defaul Wert der Combobox
combobox_hausart.bind("<<ComboboxSelected>>", lambda event: select_combobox(event, "hausart"))     # Event Handle, wird etwas ausgewählt, wird select funktion ausgeführt


# Checkbuttons Architekt, Markler, Denkmalschutz
label_checkbutton_architekt = tk.Label(window, text ="Architekt:")
label_checkbutton_architekt.grid(row=5, sticky=tk.W)
checkbutton_architekt_var = tk.IntVar()                                                                                  
checkbutton_architekt = tk.Checkbutton(window, variable=checkbutton_architekt_var)                 # Erstellt Checkbuttons und verknüft mit Variablen
checkbutton_architekt.grid(row=5, column=1, sticky=tk.W)

label_checkbutton_markler = tk.Label(window, text ="Markler:")
label_checkbutton_markler.grid(row=6, sticky=tk.W)                                                 
checkbutton_markler_var = tk.IntVar()                                                              # 1 für checked, 0 für unchecked
checkbutton_markler = tk.Checkbutton(window, variable=checkbutton_markler_var)
checkbutton_markler.grid(row=6, column=1, sticky=tk.W)

label_checkbutton_denkmalschutz = tk.Label(window, text ="Denkmalschutz:")
label_checkbutton_denkmalschutz.grid(row=7, sticky=tk.W)
checkbutton_denkmalschutz_var = tk.IntVar()
checkbutton_denkmalschutz = tk.Checkbutton(window, variable=checkbutton_denkmalschutz_var)
checkbutton_denkmalschutz.grid(row=7, column=1, sticky=tk.W)


# Userinput Entry Grundstückfläche, Wohnfläche, Baujahr
label_grundstuecksflaeche = tk.Label(window, text='Wie viel m² Grundstücksfläche?')
label_grundstuecksflaeche.grid(row=8, sticky=tk.W)             

label_wohnflaeche = tk.Label(window, text='Wie viel m² Wohnfläche?')
label_wohnflaeche.grid(row=9, sticky=tk.W)

label_baujahr = tk.Label(window, text='Welches Baujahr?')
label_baujahr.grid(row=10, sticky=tk.W)

entry_grundstuecksflaeche = tk.Entry(window)                                                                               
entry_wohnflaeche = tk.Entry(window)   
entry_baujahr = tk.Entry(window)      

entry_grundstuecksflaeche.grid(row=8, column=1)
entry_wohnflaeche.grid(row=9, column=1)
entry_baujahr.grid(row=10, column=1)


# Button Berechnug Command-Funktion
def button_berechnung_command() ->None:

   input_grundstuecksflaeche = int(entry_grundstuecksflaeche.get())
   input_wohnflaeche = int(entry_wohnflaeche.get())
   input_baujahr = int(entry_baujahr.get())
   architekt_status = checkbutton_architekt_var.get()
   markler_status = checkbutton_markler_var.get()
   denkmalschutz_status = checkbutton_denkmalschutz_var.get()

   immobilie = Immobilie(grundstuecksflaeche = input_grundstuecksflaeche,
                        wohnflaeche = input_wohnflaeche,
                        baujahr = input_baujahr
                        )
   
   schaetzwert = immobilie.berechnung(selected_bundesland,
                                    selected_region, 
                                    selected_ausstattung, 
                                    selected_hausart, 
                                    architekt_status, 
                                    markler_status, 
                                    denkmalschutz_status
                        )
   
   label_output_text.config(text = "Deine Immobilien hat den Schätzwert:")
   label_output_result.config(text = f"{schaetzwert:,}€")

# Button Berechnung
button_berechnung = tk.Button(window, text="Immobilienwert schätzen", width=25,
                               command=button_berechnung_command
                               )
button_berechnung.grid(row=11, columnspan=2)


# Label Ausgabe
label_output_text = tk.Label(window, text="")
label_output_text.grid(row=12, columnspan=2)  
label_output_result = tk.Label(window, text="")
label_output_result.grid(row=13, columnspan=2)  


# Leere Row
label_empty = tk.Label(window, text="")
label_empty.grid(row=14, columnspan=2)


def reset_all():
   # Comboboxen Anzeige
   combobox_bundesland.set("Bundesland")  
   combobox_region.set("Region")          
   combobox_ausstattung.set("Ausstattung") 
   combobox_hausart.set("Hausart")

   # Comboboxwerte
   global selected_bundesland, selected_region
   global selected_ausstattung, selected_hausart
   selected_bundesland = None                                                                # Werte auf None um später zu prüfen, ob etwas ausgewählt wurde.
   selected_region = None
   selected_ausstattung = None
   selected_hausart = None       

   # Checkbuttons
   checkbutton_architekt_var.set(0)       
   checkbutton_markler_var.set(0)         
   checkbutton_denkmalschutz_var.set(0)   

   # Entry 
   entry_grundstuecksflaeche.delete(0, tk.END)                                               # tk.END: Der Index für das Ende des Texts im Widget.
   entry_wohnflaeche.delete(0, tk.END)          
   entry_baujahr.delete(0, tk.END)              

   # Label
   label_output_text.config(text="")
   label_output_result.config(text="")

# Button Reset
button_reset = tk.Button(window, text="Reset", width=25, command=reset_all)                  # Erstellt Button mit der reset Funktion
button_reset.grid(row=15, columnspan=2)


# Leere Row
label_empty = tk.Label(window, text="")
label_empty.grid(row=16, columnspan=2)


# PDF Erstellen
def pdf_create() -> None:
   pass


# Button PDF
button_pdf = tk.Button(window, text='PDF erstellen', width=25, command=pdf_create)           # Erstellt Button mit der pdf Funktion
button_pdf.grid(row=17, columnspan=2)


# Leere Row
label_empty = tk.Label(window, text="")
label_empty.grid(row=18, columnspan=2)


# Button Exit
button_exit = tk.Button(window, text='Exit', width=25, command=window.destroy)               # Erstellt Button mit der exit Funktion
button_exit.grid(row=100, columnspan=2)

# Starten des GUI
window.config(menu=menubar)
window.mainloop()