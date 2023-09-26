import pandas as pd
import random

# Input and output file paths
input_excel_file = r"D:\WORKSPACE_LP2\FINAL_DATA\merged\neutral_Combined.xlsx"
output_excel_file =r"D:\WORKSPACE_LP2\FINAL_DATA\merged\neutral_Combined_1000.xlsx"

# Number of rows to randomly select
num_rows_to_select = 1000

# Read the input Excel file into a pandas DataFrame
df = pd.read_excel(input_excel_file)

# Check if the number of rows in the DataFrame is less than the desired number
if len(df) < num_rows_to_select:
    print("The input Excel file does not contain enough rows.")
else:
    # Randomly select 1000 rows from the DataFrame
    random_indices = random.sample(range(len(df)), num_rows_to_select)
    selected_rows = df.iloc[random_indices]

    # Save the selected rows to the output Excel file
    selected_rows.to_excel(output_excel_file, index=False, engine='openpyxl')

    print(f"Randomly selected {num_rows_to_select} rows and saved to {output_excel_file}")
