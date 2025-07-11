# Fitbit to Garmin Activity Data Converter

This Python tool converts exported Fitbit JSON data (steps, calories, distance) into a Garmin-compatible `Activities` CSV format for manual import into Garmin Connect.

---

## 📦 Features

- Parses multiple `steps-*.json`, `calories-*.json`, and `distance-*.json` files
- Aggregates by day
- Formats output as `Activities` section for Garmin Connect
- Produces a single CSV ready for import

---

## 📁 Input File Requirements

Export your data from Fitbit using Google Takeout or Fitbit Dashboard.

Expected files inside:

```
Takeout/Fitbit/GlobalExportData/
├── steps-2021-06-01.json
├── calories-2021-06-01.json
├── distance-2021-06-01.json
...
```

Each JSON file should contain entries with:

```json
[
  {
    "dateTime": "2021-06-01T00:00:00",
    "value": "1234"
  },
  ...
]
```

---

## 📤 Output

The script generates a CSV file like this:

```csv
Activities
Date,Calories Burned,Steps,Distance,Floors,Minutes Sedentary,Minutes Lightly Active,Minutes Fairly Active,Minutes Very Active,Activity Calories
2021-06-01,1234.00,4567,3.25,0,0,0,0,0,0
```

- One row per day
- `Steps`: integer
- `Distance`, `Calories Burned`: floats
- Other columns default to 0

---

## ⚙️ Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/fitbit-to-garmin.git
cd fitbit-to-garmin
```

2. Set up environment (optional):

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install pandas
```

---

## 🚀 Usage

Run the script with:

```bash
python fitbit_to_garmin.py
```

Or directly from Python:

```python
from fitbit_to_garmin import convert_fitbit_to_garmin_format

convert_fitbit_to_garmin_format(
    fitbit_folder="Takeout/Fitbit/GlobalExportData",
    output_csv="output/fitbit_to_garmin_activities.csv"
)
```

---

## 📥 Import to Garmin Connect

1. Open [Garmin Connect Web](https://connect.garmin.com/)
2. Go to **Account Settings > Import Data**
3. Upload the generated CSV file
4. Only import days **not already recorded**

---

## 🛠 Troubleshooting

### ❌ Garmin error: “The file was a valid type, but contained data we could not process”

Make sure that:
- All numbers are plain digits (no commas or quotes)
- `Steps` is an integer
- `Date` is `YYYY-MM-DD`
- All columns are present, even if values are `0`

---

## 📄 License

MIT License

---

## ✨ Credits

Built by  Inspired by Fitbit's export format and Garmin's CSV import spec.
