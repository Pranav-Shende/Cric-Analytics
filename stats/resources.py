import pandas as pd
import os
from django.conf import settings

# 1. Dynamically find the path to the CSV files in your stats folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ODI_PATH = os.path.join(BASE_DIR, "dls_odi.csv")
T20_PATH = os.path.join(BASE_DIR, "dls_t20.csv")

# 2. Load the DataFrames using the absolute paths
# Note: We use try-except here so the server doesn't crash if files are missing
try:
    odi_df = pd.read_csv(ODI_PATH).set_index("Overs_Available")
    t20_df = pd.read_csv(T20_PATH).set_index("Overs_Available")
except FileNotFoundError as e:
    print(f"⚠️ DLS CSV Error: {e}")
    odi_df = pd.DataFrame()
    t20_df = pd.DataFrame()

def get_resource(overs_left, wickets_lost, fmt):
    fmt = fmt.lower()
    table = odi_df if fmt == "odi" else t20_df
    
    # Ensure wickets_lost is treated as a string to match CSV column headers
    wicket_col = str(wickets_lost)
    
    try:
        # Round overs_left to an integer since CSV indices are usually whole numbers
        return float(table.loc[int(overs_left), wicket_col])
    except (KeyError, ValueError):
        # Fallback if the specific over/wicket combo isn't in your table
        raise ValueError(f"Invalid DLS lookup: {overs_left} overs, {wickets_lost} wickets")