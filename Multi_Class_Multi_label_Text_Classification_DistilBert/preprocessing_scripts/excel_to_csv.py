import pandas as pd

df = pd.read_csv(r"D:\FINAL_DATA\pratyaksh\Profanity_Category_Data.csv")

df.to_excel(r"D:\FINAL_DATA\pratyaksh\Profanity_Category_Data.xlsx", index=False)