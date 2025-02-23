import pandas as pd
from tkinter.filedialog import askopenfile

file = askopenfile(mode ='r', filetypes =[('Excel', '*.xlsx')])

if file is not None:
    file_path = file.name

config_df = pd.read_excel(file_path, sheet_name="Preisinfo")
print(config_df.to_string())


bundeslaender_config_dict = dict(zip(list(config_df["Bundesland"].dropna()), list(config_df["B-Kostenfaktor"].dropna())))
region_config_dict = dict(zip(list(config_df["Region"].dropna()), list(config_df["R-Kostenfaktor"].dropna())))
ausstattung_config_dict = dict(zip(list(config_df["Ausstattung"].dropna()), list(config_df["A-Kostenfaktor"].dropna())))
hausart_config_dict = dict(zip(list(config_df["Hausart"].dropna()), list(config_df["H-Kostenfaktor"].dropna())))


grundstueck_config_preis = list(config_df["Preis"])[0]
wohnflaeche_config_preis = list(config_df["Preis"])[1]

architekt_config_rate = list(config_df["Preis"])[2]
makler_config_rate = list(config_df["Preis"])[3]
denkmalschutz_config_rate = list(config_df["Preis"])[4]

baujahr_config_rate = list(config_df["Preis"])[5]
