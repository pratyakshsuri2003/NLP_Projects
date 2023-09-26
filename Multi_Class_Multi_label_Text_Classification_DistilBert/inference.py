import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification

# Load the DistilBERT tokenizer and model
tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")  # You may need to specify the correct 

model = DistilBertForSequenceClassification.from_pretrained(r"D:\WORKSPACE_LP2\FINAL_DATA\TRAINS\first_training\distilbert-youtube_text_multiclass_classification")  

mapping = {'0': 'obscenity and profanity', '1': 'Crime and Harmful Acts', '2': 'Adult', '3': 'DIY & Remedies', '4': 'Fashion', '5': 'llegal Drugs Tobacco E-cigarettes Vaping Alcohol', '6': 'Death Injury Or Military Conflict', '7': 'Pranks', '8': 'Spam', '9': 'Food', '10': 'Gambling', '11': 'Terrorism', '12': 'Debated Issues', '13': 'Education', '14': 'Cartoon', '15': 'Gaming', '16': 'Sports & Fitness', '17': 'Religious', '18': 'Neutral'}

# Input text for inference
input_text = "charas vaping and cigerrates"

# Tokenize input text
input_ids = tokenizer.encode(input_text, add_special_tokens=True, truncation=True, padding=True, return_tensors="pt")

# Perform inference
with torch.no_grad():
    outputs = model(input_ids)

# Get the predicted class probabilities
logits = outputs.logits
predicted_class = torch.argmax(logits, dim=1).item()
predicted_probabilities = torch.softmax(logits, dim=1).tolist()[0]

# Look up the class name from the mapping
predicted_class_name = mapping.get(str(predicted_class), "Unknown Class")

# Print results
print(f"Input Text: {input_text}")
print(f"Predicted Class: {predicted_class} ({predicted_class_name})")
print(f"Predicted Probabilities: {predicted_probabilities}")

