import pandas as pd

# Define the input Excel file and the category list
input_file = r"D:\WORKSPACE_LP2\FINAL_DATA\merged\All_Category_Data_Combined_preprocessed_tags_removed_CLEANED.xlsx"
category_list = ["Cartoon", "Food", "Religious", "Terrorism", "Education"]  # Replace with your category names

# Read the Excel file into a Pandas DataFrame
df = pd.read_excel(input_file)

# Iterate through the category list
for category in category_list:
    # Filter rows based on the 'actual' column matching the category
    filtered_df = df[df['actual'] == category]

    # Check if there are more than 500 rows for the category
    if len(filtered_df) > 500:
        filtered_df = filtered_df.head(500)  # Take the first 500 rows

    # Create a new Excel file for the category
    output_file = f"{category}_output.xlsx"

    # Save the filtered DataFrame to the output Excel file
    filtered_df.to_excel(output_file, index=False)

    print(f"{len(filtered_df)} rows saved for {category} in {output_file}")
