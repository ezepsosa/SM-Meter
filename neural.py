import os
from tokenize import Double
import numpy as np
import tensorflow as tf
from tensorflow import keras
from transformers import BertTokenizer
import re
def text_preprocessing(s):
    s = s.lower()
    #Remove links
    s = re.sub(r"http\S+", "", s)
    # Change 't to 'not'
    s = re.sub(r"\'t", " not", s)
    # Remove @name
    s = re.sub("@[A-Za-z0-9_]+","", s)
    # Remove hashtags
    s = re.sub("#[A-Za-z0-9_]+","", s)
    # Remove rt
    s = re.sub(r'(@.*?)[\s]', ' ', s)
    # Isolate and remove punctuations except '?'
    s = re.sub(r'([\'\"\.\(\)\!\?\\\/\,])', r' \1 ', s)
    
    s = re.sub(r'[^\w\s\?]', ' ', s)
    # Remove some special characters
    s = re.sub(r'([\;\:\|•«\n])', ' ', s)
    # Remove trailing whitespace
    s = re.sub(r"\brt\b", "", s)
    # Remove numbers
    s = re.sub(r'\d+', '', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def prepare_data(input_text, tokenizer):
    token = tokenizer.encode_plus(
        input_text,
        max_length=150, 
        truncation=True, 
        padding='max_length', 
        add_special_tokens=True,
        return_tensors='tf'
    )
    return {
        'input_ids': tf.cast(token.input_ids, tf.float64),
        'attention_mask': tf.cast(token.attention_mask, tf.float64)
    }
    

def predict(model, processed_data, classes):
    probs = model.predict(processed_data)[0]
    return classes[np.argmax(probs)], probs[np.argmax(probs)]

def predict_sentiment_twitter_eng(input_data, model):
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    data = prepare_data(text_preprocessing(input_data), tokenizer)
    classPredicted, acc = predict(model, data, ["Negative", "Positive"])
    return classPredicted + ": " + str(round(acc, 2))

def load_model(path):
    return tf.keras.models.load_model(path)
