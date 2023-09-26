import tensorflow as tf
import pandas as pd
from sklearn.model_selection import train_test_split
from transformers import DistilBertTokenizer, TFDistilBertForSequenceClassification
import pickle

# Define constants
MODEL_NAME = 'distilbert-base-uncased'
MAX_LEN = 512
TEST_SPLIT = 0.2
BATCH_SIZE = 16
N_EPOCHS = 100
THRESHOLD = 0.5

# Read the Excel file
df = pd.read_excel("/home/pratyaksh.suri/Distilbert_Dataset/Cleaned_50_5_category_test_preprocessed_stopwords.xlsx")

x = df["text"].astype(str).tolist()
y = df["actual"].tolist()

# Encode labels using LabelEncoder
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Split the data into training and test sets while maintaining class proportions
x_train, x_test, y_train, y_test = train_test_split(x, y_encoded, test_size=TEST_SPLIT, stratify=y_encoded, random_state=42)

# Initialize the tokenizer and model
tkzr = DistilBertTokenizer.from_pretrained(MODEL_NAME)
model = TFDistilBertForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=len(le.classes_))

# Create TensorFlow datasets for training and test
def construct_encodings(x, tkzr, max_len, trucation=True, padding=True):
    return tkzr(x, max_length=max_len, truncation=trucation, padding=padding)

encodings_train = construct_encodings(x_train, tkzr, max_len=MAX_LEN)
encodings_test = construct_encodings(x_test, tkzr, max_len=MAX_LEN)

def construct_tfdataset(encodings, y=None):
    if y is not None:
        return tf.data.Dataset.from_tensor_slices((dict(encodings), y))
    else:
        return tf.data.Dataset.from_tensor_slices(dict(encodings))

tfdataset_train = construct_tfdataset(encodings_train, y_train).batch(BATCH_SIZE)
tfdataset_test = construct_tfdataset(encodings_test, y_test).batch(BATCH_SIZE)

# Define a callback to save the best model and model at the end of each epoch
checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
    "./model4/model_epoch_{epoch:02d}",
    monitor='val_accuracy',  # Monitoring validation accuracy
    save_best_only=True,     # Save only the best model
    mode='max',              # Save the model when validation accuracy is maximized
    save_weights_only=True,  # Save only the model weights
    save_format='tf'         # Save as a TensorFlow SavedModel
)

# Compile the model
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=['accuracy']
)

# Train the model
history = model.fit(
    tfdataset_train,
    epochs=N_EPOCHS,
    validation_data=tfdataset_test,
    callbacks=[checkpoint_callback]  # Use the checkpoint callback
)

# Save the best model
best_model_path = "./model4/best_model"
model.save_pretrained(best_model_path)

# Save model info
with open('model_info.pkl', 'wb') as f:
    pickle.dump((MODEL_NAME, MAX_LEN, le.classes_), f)

# Define a function to create a predictor
def create_predictor(model, model_name, max_len, num_labels):
    tkzr = DistilBertTokenizer.from_pretrained(model_name)

    def predict_proba(text):
        x = [text]
        encodings = construct_encodings(x, tkzr, max_len=max_len)
        tfdataset = construct_tfdataset(encodings)
        tfdataset = tfdataset.batch(1)

        preds = model.predict(tfdataset).logits
        preds = tf.nn.softmax(preds, axis=-1).numpy()
        return preds[0]

    return predict_proba

# Define a function to predict categories with probabilities
def predict_categories(text, clf, threshold):
    preds = clf(text)
    labels = [le.inverse_transform([i])[0] for i in range(len(preds))]
    categories = [label for label, prob in zip(labels, preds) if prob >= threshold]
    return categories

# Example usage of the predictor
clf = create_predictor(model, MODEL_NAME, MAX_LEN, len(le.classes_))
text = 'doraemon and shinchan are best friends.'
predicted_categories = predict_categories(text, clf, THRESHOLD)
print(predicted_categories)

# Load the best model and model info
loaded_best_model = TFDistilBertForSequenceClassification.from_pretrained(best_model_path)
model_name, max_len, classes = pickle.load(open("model_info.pkl", 'rb'))

# Use the loaded model to create a predictor
clf = create_predictor(loaded_best_model, model_name, max_len, len(classes))
print(clf('doraemon and shinchan are best friends.'))
