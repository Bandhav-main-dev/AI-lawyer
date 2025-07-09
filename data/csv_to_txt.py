import pandas as pd
import os

# Load CSV without headers
df = pd.read_csv("/home/user123/Bandhav_project/AI_lawyer/data/bare_acts/ipc_sections.csv", header=None)

# Rename columns manually based on your previous output
df.columns = ["Description", "Title", "Punishment", "Section"]

# Fill NaN values with empty string (to avoid float errors)
df = df.fillna("")

# Create directory for output .txt files
output_dir = "data/bare_acts/ipc"
os.makedirs(output_dir, exist_ok=True)

# Write each row to a text file
for _, row in df.iterrows():
    section = str(row['Section']).replace("IPC_", "").strip()
    title = str(row['Title']).strip()
    description = str(row['Description']).strip()
    punishment = str(row['Punishment']).strip()

    filename = f"{output_dir}/section_{section}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"{title}\n\n{description}\n\nPunishment: {punishment}")
    print(f"Created file: {filename}")