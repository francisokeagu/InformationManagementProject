# To Verify sample data for project

import pandas as pd
import os

# Path to your dataset folder
data_path = "data/library_management_system"

# Loop through each file in the dataset folder
for file in os.listdir(data_path):
    if file.endswith(".csv"):
        print(f"\n--- {file} ---")
        df = pd.read_csv(os.path.join(data_path, file))
        print(df.head())  # Show the first 5 rows
