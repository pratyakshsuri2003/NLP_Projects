import os

# Specify the parent directory where the CSV files are located
parent_directory = r'D:/BACKUP/grouped_csvs'
output_txt_file = 'output.txt'

# Function to recursively find CSV file names in subdirectories
def find_csv_file_names(directory):
    csv_file_names = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.csv'):
                csv_file_names.append(file)
    return csv_file_names

# Find all CSV file names in subdirectories
csv_file_names = find_csv_file_names(parent_directory)

# Save the CSV file names to the output text file
with open(output_txt_file, 'w') as txt_file:
    for csv_file_name in csv_file_names:
        txt_file.write(csv_file_name + '\n')

print(f'CSV file names in subdirectories have been saved to {output_txt_file}')
