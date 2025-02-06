import reportlab as rl   # erstellt pdfs
import pandas as pd      # pandas kann Excel Dateien lesen
import tkinter as tk     # Gui graphical user interface
from tkinter import  ttk # ttk muss explizit extra importiert werden
import datetime as dt    # Für das aktuelle Jahr
import os                # Filemanagment

# Standardwerte für Kostenfaktoren
bundeslaender_standard_dict = {
                     "Baden-Württemberg": 1.5,
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

region_standard_dict = {
               "Land": 1,
               "Stadt": 2
               }

ausstattung_standard_dict = {
                  "Rohbau": 0.5,
                  "Sanierungsbedarf": 0.8,
                  "Renovierungsbedarf": 0.9,
                  "Einfach": 1.0,
                  "Gehoben": 2.0
                  }

hausart_standard_dict = {
               "Einfamilienhaus": 1,
               "Doppelhaushälfte": 0.8,
               "Mehrfamilienhaus": 0.7
               }

grundstueck_standard_preis = 160
wohnflaeche_standard_preis = 2500

architekt_standard_rate = 0.2
makler_standard_rate = 0.02
denkmalschutz_standard_rate = 0.20

baujahr_standard_rate = 0.001


class Immobilie:
   
   
   def __init__(self,
                bundeslaender_dict:dict = bundeslaender_standard_dict,
                region_dict:dict = region_standard_dict,
                ausstattung_dict:dict = ausstattung_standard_dict,
                hausart_dict:dict = hausart_standard_dict,
                grundstueck_preis:int = grundstueck_standard_preis,
                wohnflaeche_preis:int = wohnflaeche_standard_preis,
                architekt_rate:float = architekt_standard_rate,
                makler_rate:float = makler_standard_rate,
                denkmalschutz_rate:float = denkmalschutz_standard_rate,
                baujahr_rate:float = baujahr_standard_rate,
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
      self.baujahr = baujahr



   def berechnung(self, selected_bundesland, select,  bool, bool, bool)

      check() #eingebene sachen
      checkannutzer()# stimmen die eingaben ?
      result = KI.bundesland_dict[selected_bundesland] * KI.redion_dict[selected_region] * ....
      tk.Label(window, text = result)
      return result


# window

tk.Button(window, text="berechnen" command=KI.berechnug(variablen))


tk.Label(window, text= )


config laden ? impoprt os

immobilie = Immobilie()

window.mainloop()