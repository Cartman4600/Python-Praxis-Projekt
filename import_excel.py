import pandas as pd

config_df = pd.read_excel(r"repc_config.xlsx", sheet_name="Preisinfo")

print(config_df.to_string())

print(config_df["Bundesland"])