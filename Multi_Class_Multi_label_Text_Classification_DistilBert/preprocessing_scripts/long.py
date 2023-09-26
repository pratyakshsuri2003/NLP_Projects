import pandas as pd

# Replace 'input_file.xlsx' and 'Sheet1' with your Excel file and sheet name
input_file = r"D:\WORKSPACE_LP2\FINAL_DATA\merged\small_dataset\1500\1500_300_per_class_5_classes_dataset.xlsx"
output_file = r"D:\WORKSPACE_LP2\FINAL_DATA\merged\small_dataset\1500\1500_300_per_class_5_classes_dataset_cleaned.xlsx"

# Load the Excel file into a DataFrame
df = pd.read_excel(input_file)

# Define a function to count the number of lines in a cell
def count_lines(text):
    lines = text.split('\n')
    print("Doing ...")
    return len(lines)

# Filter rows where the text has 5 or fewer lines
df = df[df['text'].apply(count_lines) <= 5]

# Save the updated DataFrame back to a new Excel file
df.to_excel(output_file, index=False, engine='openpyxl')
print("SUCCESS !!")

