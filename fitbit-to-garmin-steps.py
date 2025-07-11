import os
import pandas as pd
from pathlib import Path

def read_fitbit_json(folder: Path, prefix: str, column_name: str, round_int=False):
    data_frames = []
    for file in folder.glob(f"{prefix}*.json"):
        try:
            df = pd.read_json(file)
            df["date"] = pd.to_datetime(df["dateTime"], errors='coerce').dt.date
            df["value"] = pd.to_numeric(df["value"], errors='coerce')
            df = df.dropna(subset=["date", "value"])
            if round_int:
                df["value"] = df["value"].round().astype(int)
            daily = df.groupby("date", as_index=False)["value"].sum()
            daily.rename(columns={"value": column_name}, inplace=True)
            data_frames.append(daily)
        except Exception as e:
            print(f"Error reading {file.name}: {e}")
    if data_frames:
        return pd.concat(data_frames).groupby("date", as_index=False).sum()
    return pd.DataFrame(columns=["date", column_name])

def convert_fitbit_to_garmin_format(fitbit_folder: str, output_csv: str):
    folder_path = Path(fitbit_folder)

    # Read metrics
    steps_df = read_fitbit_json(folder_path, "steps", "Steps", round_int=True)
    cal_df = read_fitbit_json(folder_path, "calories", "Calories Burned")
    dist_df = read_fitbit_json(folder_path, "distance", "Distance")

    # Merge on date
    combined = pd.merge(steps_df, cal_df, on="date", how="outer")
    combined = pd.merge(combined, dist_df, on="date", how="outer")
    combined.fillna(0, inplace=True)

    # Garmin-required fields
    combined["Floors"] = 0
    combined["Minutes Sedentary"] = 0
    combined["Minutes Lightly Active"] = 0
    combined["Minutes Fairly Active"] = 0
    combined["Minutes Very Active"] = 0
    combined["Activity Calories"] = 0

    # Format Date
    combined["Date"] = combined["date"].astype(str)

    # Ensure all columns are in proper type
    cols_int = ["Steps", "Floors", "Minutes Sedentary", "Minutes Lightly Active", 
                "Minutes Fairly Active", "Minutes Very Active", "Activity Calories"]
    cols_float = ["Calories Burned", "Distance"]

    for col in cols_int:
        combined[col] = combined[col].astype(int)
    for col in cols_float:
        combined[col] = combined[col].astype(float)

    garmin_columns = [
        "Date", "Calories Burned", "Steps", "Distance", "Floors",
        "Minutes Sedentary", "Minutes Lightly Active", "Minutes Fairly Active",
        "Minutes Very Active", "Activity Calories"
    ]
    garmin_df = combined[garmin_columns].sort_values("Date")

    # Save CSV with proper formatting
    with open(output_csv, "w", encoding="utf-8", newline='') as f:
        f.write("Activities\n")
        garmin_df.to_csv(f, index=False, float_format="%.2f")

    print(f"✅ Garmin CSV saved to: {output_csv}")

# Example usage
convert_fitbit_to_garmin_format(
    fitbit_folder="Takeout/Fitbit/GlobalExportData",
    output_csv="fitbit_to_garmin_activities.csv"
)
