import csv
import string

def contains_non_ascii_and_special(text):
    special_characters = [
        "âž¡ï¸", "ðŸ¦", "ðŸ“²", "ðŸ“¸", "ðŸ’»",
        "ð—¨ð—Ÿ", "ð—œð—”ð—”ð— ", "â€‹â€‹ð‘»ð‘¬ð‘¨ð‘´", "ð‘«ð‘°ð‘¹ð‘¬ð‘ªð‘»ð‘¶ð‘¹", "ð‘¨ð‘³ð‘´ð‘¨ð‘µ", "ð‘¨ð‘©ð‘«ð‘¼ð‘³ð‘³ð‘¨ð‘¯",
        "â†’Â", "ð‘»ð’‰ð’Šð’”", "ð’„ð’ð’•ð’•ð’†ð’ð’•", "ð’Šð’”", "ð’„ð’ð’šð’“ð’Šð’‰ð’‰ð’•ð’†ð’…", "ð’•ð’", "ð‘¨ð’", "ð’ˆð’‚ð’‚ð’•ð’ð’Šð’Šð’†ð’†ð’…ð’†", "ï†",
        "â€¢", "â–º", "â€¢", "à","¦","?à","¦", "à","¦¶ à","¦«à¦","²à§?à¦","° à", "Â°"
    ]
    
    special_characters_set = set(special_characters)
    printable_characters = set(string.printable)
    
    for char in text:
        if char not in printable_characters or char in special_characters_set:
            return True
    return False

def remove_rows_with_special_character(input_file, output_file, col_names):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for row in reader:
            should_remove = False
            
            for col_name in col_names:
                col_text = row[col_name]
                
                if contains_non_ascii_and_special(col_text):
                    should_remove = True
                    break  # No need to check further for this row
                
            if not should_remove:
                writer.writerow(row)

if __name__ == "__main__":
    input_csv = r"C:\Users\LP-197\Downloads\illegal_drugs_data1.csv"
    output_csv = r"C:\Users\LP-197\Downloads\illegal_drugs_data1_cleaned.csv"
    target_col_names = ["title", "description", "tags"]  # Replace with the names of the columns you want to check
    
    remove_rows_with_special_character(input_csv, output_csv, target_col_names)
