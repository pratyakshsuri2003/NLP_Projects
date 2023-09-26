import pandas as pd
import re
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import warnings

# Ignore FutureWarnings for str.replace
warnings.simplefilter(action='ignore', category=FutureWarning)

# Download the NLTK stopwords if not already downloaded
nltk.download('stopwords')
nltk.download('punkt')

def remove_stopwords(text):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text)
    filtered_words = [word for word in words if word.lower() not in stop_words]
    return ' '.join(filtered_words)

# Function to remove URLs from text
def remove_urls(text):
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    return re.sub(url_pattern, '', text)

words_to_remove = ['subscribe', 'click this', 'click', 'click here', 'twitter', 'insta', 'instagram', 'follow', 'like share', 'channel', 'hello guys welcome', 'to my youtube', 'youtube channel', 'follow this page', 'click this link to follow my page', 'click this link to follow', 'follow me on insta', 'follow me on instagram']

def remove_words(text):
    for word in words_to_remove:
        text = text.replace(word, '')
    return text

if __name__ == "__main__":

    input_excel = r"D:\WORKSPACE_LP2\FINAL_DATA\merged\All_Category_Data_Combined.xlsx"
    output_excel = r"D:\WORKSPACE_LP2\FINAL_DATA\merged\All_Category_Data_Combined_DDDDDDDDDDDDDDDDDDDDD.xlsx"
    
    # Reading the excel
    input_df = pd.read_excel(input_excel)

    # Define the columns you need
    #columns_needed = ['input_url', 'actual', 'title', 'description', 'tags'] # OLD
    columns_needed = ['input_url' ,'actual', 'title', 'description'] # NEW
    input_df = input_df[columns_needed]
    print("Check-1: Columns Needed [Done]")

    # Remove nan values
    input_df["title"].fillna("", inplace=True)
    input_df["description"].fillna("", inplace=True)
    
    # Remove newlines
    input_df['title'] = input_df['title'].str.replace('\n', ' ')
    input_df['description'] = input_df['description'].str.replace('\n', ' ')
    print("Check-2: Remove newlines [Done]")

    # Remove Stopwords
    #input_df['text'] = input_df['text'].apply(remove_stopwords)
    # input_df['description'] = input_df['description'].apply(lambda x: remove_stopwords(str(x)))
    # print("Check-3: Remove Stopwords [Done]")

    # Merge
    input_df['text'] = input_df['title'] + " " +input_df['description']

    # Remove numbers
    input_df['text'] = input_df['text'].str.replace(r'\d+', '') 
    print("Check-4: Remove numbers [Done]") 

    # Convert text to lowercase
    input_df['text'] = input_df['text'].str.lower()
    print("Check-5: Convert text to lowercase [Done]") 
    
    # Remove special characters
    special_characters = r'[@#!$%^*]'
    input_df['text'] = input_df['text'].str.replace(special_characters, '', regex=True)
    print("Check-6: Remove special characters and Punctuations [Done]")

    # Apply the remove_urls function to the 'text' column
    input_df['text'] = input_df['text'].apply(lambda x: remove_words(str(x)))
    #input_df['description'] = input_df['description'].apply(lambda x: remove_urls(str(x)))
    print("Check-7: Remove URLS [Done]")

    # Apply the remove_words function to the specified column
    words_to_remove = ['subscribe', 'click this', 'click', 'click here', 'twitter', 'insta', 'instagram', 'follow', 'like share', 'channel', 'hello guys welcome', 'to my youtube', 'youtube channel', 'follow this page', 'click this link to follow my page', 'click this link to follow', 'follow me on insta', 'follow me on instagram']
    input_df['text'] = input_df['text'].apply(remove_words)
    print("Check-3: Remove Social media words [Done]")

    # Remove digits
    input_df['text'] = input_df['text'].str.replace(r'\d+', '', regex=True)
    print("Check-8: Remove Digits [Done]")
    
    input_df['text'] = input_df['text'].str.replace('#', '')

    # Remove '@' character from the "tags" column
    input_df['text'] = input_df['text'].str.replace('@', '')

    # Replace & with 'and'
    input_df['text'] = input_df['text'].str.replace('&', 'and')

    input_df['text'] = input_df['text'].str.replace('https', '')

    input_df['text'] = input_df['text'].str.replace('HTTP', '')

    input_df['text'] = input_df['text'].str.replace('http', '')

    input_df['text'] = input_df['text'].str.replace('click here', '')

    input_df['text'] = input_df['text'].str.replace('twitter', '')

    input_df['text'] = input_df['text'].str.replace('twitter', '')
    
    # Remove slashes
    input_df['text'] = input_df['text'].str.replace('/', '')
    
    # Remove tilde
    input_df['text'] = input_df['text'].str.replace('~', '')
    
    # Remove commas
    input_df['text'] = input_df['text'].str.replace(',', '')
    
    # Remove duplicate slashes (//)
    input_df['text'] = input_df['text'].str.replace('//', '')
    
    # Remove vertical bar (|)
    input_df['text'] = input_df['text'].str.replace('|', '')

    # Remove vertical bar ('(')
    input_df['text'] = input_df['text'].str.replace('(', '')

    # Remove vertical bar (')')
    input_df['text'] = input_df['text'].str.replace(')', '')

    # Remove vertical bar ('[')
    input_df['text'] = input_df['text'].str.replace('[', '')

    # Remove vertical bar (']')
    input_df['text'] = input_df['text'].str.replace(']', '')

    # Remove vertical bar ('.')
    input_df['text'] = input_df['text'].str.replace('.', '')

    # Remove vertical bar ('"')
    input_df['text'] = input_df['text'].str.replace('"', '')

    # Remove vertical bar ('``')
    input_df['text'] = input_df['text'].str.replace('``', '')

    # Remove vertical bar ('_')
    input_df['text'] = input_df['text'].str.replace('_', '')

    # Remove vertical bar ('__')
    input_df['text'] = input_df['text'].str.replace('__', '')

    # Remove vertical bar ('?')
    input_df['text'] = input_df['text'].str.replace('?', '')

    # Remove vertical bar (''s')
    input_df['text'] = input_df['text'].str.replace("'s", '')

    # Remove vertical bar ("'")
    input_df['text'] = input_df['text'].str.replace("'", '')

    # Remove vertical bar ("+")
    input_df['text'] = input_df['text'].str.replace("+", '')

    # Remove vertical bar ('-')
    input_df['text'] = input_df['text'].str.replace('-', '')

    # Remove vertical bar (':')
    input_df['text'] = input_df['text'].str.replace(':', '')

    # Remove vertical bar (';')
    input_df['text'] = input_df['text'].str.replace(';', '')

    # Remove vertical bar ('=')
    input_df['text'] = input_df['text'].str.replace('=', '')

    # Remove vertical bar ('*')
    input_df['text'] = input_df['text'].str.replace('*', '') 

    # Drop NaN and duplicates
    input_df.dropna(inplace=True)
    print("Check-9: Remove Empty Rows [Done]")
    
    input_df.drop_duplicates(inplace=True)
    print("Check-10: Remove Duplicates [Done]")
    
    # Save to output Excel file
    input_df.to_excel(output_excel, index=False)

    print("**************************************** SUCCESS! ***********************************************")
