import pandas as pd

# Load your Excel file
excel_file_path = r"D:\FINAL_DATA\pratyaksh\Illegal Drugs Tobacco E-cigarettes Vaping Alcohol (ebin 250).xlsx"
df = pd.read_excel(excel_file_path)

# Group data by the 'Category' column
grouped = df.groupby('actual')

# Iterate through each group and save to separate Excel files
for name, group in grouped:
    # Create a new Excel writer object
    writer = pd.ExcelWriter(f'D:\scripts\csvs\\illegal_drugs\{name}.xlsx', engine='openpyxl')
    group.to_excel(writer, index=False, sheet_name=name)
    writer.save()

print("Separate Excel files created successfully.")
