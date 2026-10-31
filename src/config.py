from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "European_Bank.csv"
MODEL_PATH = BASE_DIR / "data" / "model.json"

# Required Schema
REQUIRED_COLUMNS = {
    "CustomerId",
    "Balance",
    "EstimatedSalary",
    "NumOfProducts",
    "IsActiveMember",
    "Exited",
}

# Northstar Design System Palette
PALETTE = {
    "ink": "#172521",
    "muted": "#7c8983",
    "subtle": "#98a19c",
    "line": "#e9ede8",
    "bg": "#f6f7f4",
    "panel": "#ffffff",
    "green": "#11785f",
    "green_light": "#eaf6ef",
    "mint": "#70d1aa",
    "mint_light": "#e7f3ed",
    "navy": "#183c35",
    "blue": "#526eeb",
    "blue_light": "#eef0ff",
    "amber": "#e4a43d",
    "amber_light": "#fff5e7",
    "red": "#de5442",
    "red_light": "#fef0ed",
    "violet": "#8b65c9",
    "violet_light": "#f2edfc",
}
