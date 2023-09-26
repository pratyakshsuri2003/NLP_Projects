import pandas as pd

# Load the Excel file
input_file = r"D:\WORKSPACE_LP2\FINAL_DATA\merged\All_Category_Data_Combined_preprocessed.xlsx"
output_file = r"D:\WORKSPACE_LP2\FINAL_DATA\merged\neutral_Combined.xlsx"

# Replace 'YourKeyword' with the keyword you want to match
keyword = 'Neutral'

# Read the Excel file into a DataFrame
df = pd.read_excel(input_file)

# Fill NaN values in the 'actual' column with an empty string
df['actual'].fillna('', inplace=True)

# Filter rows where the 'actual' column contains the keyword
filtered_df = df[df['actual'].str.contains(keyword, case=False)]

# Save the filtered DataFrame to a new Excel file
filtered_df.to_excel(output_file, index=False)

print(f"Matching rows saved to {output_file}")
