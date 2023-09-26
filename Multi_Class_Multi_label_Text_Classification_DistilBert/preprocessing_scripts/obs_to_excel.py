import pyexcel_ods
import pandas as pd

# Load the .ods file
ods_file_path = r"D:\FINAL_DATA\pratyaksh\Illegal Drugs Tobacco E-cigarettes Vaping Alcohol (ebin 250).ods"
data = pyexcel_ods.get_data(ods_file_path)

# Assuming the first sheet contains the data
sheet_name = list(data.keys())[0]
df = pd.DataFrame(data[sheet_name])

# Specify the output .xlsx file name
xlsx_output_path = r"D:\FINAL_DATA\pratyaksh\Illegal Drugs Tobacco E-cigarettes Vaping Alcohol (ebin 250).xlsx"

# Save the DataFrame as an .xlsx file
df.to_excel(xlsx_output_path, index=False)

print(f'Conversion completed. File saved as {xlsx_output_path}')
