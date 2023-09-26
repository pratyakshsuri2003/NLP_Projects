import pandas as pd

# Load the Excel file
df = pd.read_excel(r"D:\WORKSPACE_LP2\FINAL_DATA\grouped_csvs\illegal_drugs\illegal_merged.xlsx")

# Define a list of possible endings
possible_endings = ['!', '$', '%', '&', '/', ';', '?', '|', '~']

# Define a function to process text based on punctuation at the end
def process_text(row):
    concatenated_text = ''
    
    # Process "title" column
    if not pd.isna(row['title']):
        if row['title'].endswith(tuple(possible_endings)):
            concatenated_text += row['title']
        else:
            concatenated_text += row['title'] + ". "

    # Process "description" column
    if not pd.isna(row['description']):
        if row['description'].endswith(tuple(possible_endings)):
            concatenated_text += ' ' + row['description']
        else:
            concatenated_text += ' ' + row['description'] + ". "

    # Process "tags" column
    if not pd.isna(row['tags']):
        if row['tags'].endswith(tuple(possible_endings)):
            concatenated_text += ' ' + row['tags']
        else:
            concatenated_text += ' ' + row['tags'] + ". "

    return concatenated_text

# Apply the custom function to create the "combined_text" column
df['text'] = df.apply(process_text, axis=1)

# Save the new DataFrame to a new Excel file
df.to_excel(r"D:\WORKSPACE_LP2\FINAL_DATA\grouped_csvs\illegal_drugs\illegal_merged_concat.xlsx", index=False)
