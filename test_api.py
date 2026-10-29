import pandas as pd
import requests

csv_path = "data/CICIoT2023/raw/MERGED_CSV/MERGED_CSV/Merged01.csv"

# Use the first test-window records from the same dataset
df = pd.read_csv(csv_path)
records = df.drop(columns=["Label"]).iloc[0].tolist()

response = requests.post(
    "http://127.0.0.1:5000/predict_broad",
    json={"records": records}
)

print(response.json())
print("HTTP Status:", response.status_code)
print("API Test:", "PASSED" if response.status_code == 200 else "FAILED")