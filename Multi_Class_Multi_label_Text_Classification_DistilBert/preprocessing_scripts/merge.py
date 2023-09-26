import pandas as pd

# Load data from the first CSV file
df1 =  pd.read_excel(r"D:\FINAL_DATA\grouped_csvs\abuse\abuse_and_abuse_support.xlsx")
df2 =  pd.read_excel(r"D:\FINAL_DATA\grouped_csvs\abuse\crime.xlsx")
df3 =  pd.read_excel(r"D:\FINAL_DATA\grouped_csvs\abuse\hatespeech.xlsx")
df4 =  pd.read_excel(r"D:\FINAL_DATA\grouped_csvs\abuse\neutral.xlsx")
df5 =  pd.read_excel(r"D:\FINAL_DATA\grouped_csvs\abuse\profane.xlsx")
df6 =  pd.read_excel(r"D:\FINAL_DATA\grouped_csvs\adult\adult.xlsx")
df7 =  pd.read_excel(r"D:\FINAL_DATA\grouped_csvs\adult\neutral.xlsx")
df8 =  pd.read_excel(r"D:\FINAL_DATA\grouped_csvs\crime\Crime.xlsx")
df9 =  pd.read_excel(r"D:\FINAL_DATA\grouped_csvs\crime\neutral.xlsx")
df10 = pd.read_excel(r"D:\FINAL_DATA\grouped_csvs\debated_issues\debated_issues.xlsx")
df10 = pd.read_excel(r"D:\FINAL_DATA\grouped_csvs\debated_issues\neutral.xlsx")
df11 = pd.read_excel(r"D:\FINAL_DATA\grouped_csvs\diy_and_remidies\Diy_and_remidies.xlsx")
df12 = pd.read_excel(r"D:\FINAL_DATA\grouped_csvs\diy_and_remidies\neutral.xlsx")
df13 = pd.read_excel(r"D:\FINAL_DATA\grouped_csvs\fashion\fashion.xlsx")
df14 = pd.read_excel(r"D:\FINAL_DATA\grouped_csvs\hatespeech\hatespeech.xlsx")
df15 = pd.read_excel(r"D:\FINAL_DATA\grouped_csvs\heavy_use_of_profane\neutral.xlsx")
df16 = pd.read_excel(r"D:\FINAL_DATA\grouped_csvs\heavy_use_of_profane\profane.xlsx")
df17 = pd.read_excel(r"D:\FINAL_DATA\grouped_csvs\illegal_drugs\illegal.xlsx")
df18 = pd.read_excel(r"D:\FINAL_DATA\grouped_csvs\illegal_drugs\neutral.xlsx")
df19 = pd.read_excel(r"D:\FINAL_DATA\grouped_csvs\military_sohang\military.xlsx")
df20 = pd.read_excel(r"D:\FINAL_DATA\grouped_csvs\pranks\neutral.xlsx")
df21 = pd.read_excel(r"D:\FINAL_DATA\grouped_csvs\pranks\prank.xlsx")
df22 = pd.read_excel(r"D:\FINAL_DATA\grouped_csvs\profanity\neutral.xlsx")
df23 = pd.read_excel(r"D:\FINAL_DATA\grouped_csvs\profanity\Profanity.xlsx")
df24 = pd.read_excel(r"D:\FINAL_DATA\grouped_csvs\spam\spam.xlsx")
df25 = pd.read_excel(r"D:\FINAL_DATA\grouped_csvs\terrorism\terrorism.xlsx")

# Combine the two DataFrames using concat or merge
combined_df = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8, df9, df10, df11, df12, df13, df14, df15, df16, df17, df18, df19, df20, df21, df22, df23, df24, df25])

# Drop duplicates based on a specific column (e.g., 'column_name')
column_name = 'input_url'
combined_df.drop_duplicates(subset=column_name, keep='first', inplace=True)

# Save the resulting DataFrame to a new CSV file
combined_df.to_csv('All_Category_Data_Combined.csv', index=False)
print("SUCCESS")
