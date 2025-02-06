import pandas as pd

df = pd.read_excel(r"Python Projekt\immobilien_preis_berechnung.xlsx", sheet_name="Preisinformationen")

print(df.to_string())