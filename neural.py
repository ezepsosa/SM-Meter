import os
from tokenize import Double
from easyprocess import unidecode
import numpy as np
import tensorflow as tf
from tensorflow import keras
from transformers import BertTokenizer
import re

tokenizer_esp = BertTokenizer.from_pretrained('dccuchile/bert-base-spanish-wwm-uncased')
tokenizer_eng = BertTokenizer.from_pretrained('bert-base-uncased')
sa_tw_model = None
sa_rd_model = None
sa_esp_model = None
aa_tw_model = None
aa_rd_model = None
aa_esp_model = None

# Method that returns the state of a neural model at that moment.
def model_status():
    global sa_tw_model,aa_tw_model, sa_rd_model, aa_rd_model, sa_esp_model, aa_esp_model 
    return [sa_tw_model,aa_tw_model, sa_rd_model, aa_rd_model, sa_esp_model, aa_esp_model ]

# Method that deactivates a neural model passed by parameters.
def disable_model(index, btn, image):
    global sa_tw_model,aa_tw_model, sa_rd_model, aa_rd_model, sa_esp_model, aa_esp_model 
    btn.configure(image=image)
    if(index == 0):
        sa_tw_model = None
    elif(index == 1):
        aa_tw_model = None
    elif(index == 2):
        sa_rd_model = None
    elif(index == 3):
        aa_rd_model = None
    elif(index == 4):
        sa_esp_model = None
    else:
        aa_esp_model = None

# Method that activate a neural model passed by parameters.
def activate_model(index,btn, image):
    btn.configure(image=image)
    if(index == 0):
        load_models(0,1,1,0,1,0)
    elif(index == 1):
        load_models(0,1,1,0,0,1)
    elif(index == 2):
        load_models(0,1,0,1,1,0)
    elif(index == 3):
        load_models(0,1,0,1,0,1)
    elif(index == 4):
        load_models(1,0,0,0,1,0)
    else:
        load_models(1,0,1,0,0,1)

# Method that activates the models according to the parameters passed, if they are already active it does not perform the operation. 
def load_models(esp, eng, tw, rd, sa, aa):
    global sa_tw_model, sa_rd_model, sa_esp_model, aa_tw_model, aa_rd_model, aa_esp_model 
    if((sa * eng * tw == 1) and not sa_tw_model):
        sa_tw_model = load_model('models/SA_TW')
    if((aa * eng * tw == 1) and not aa_tw_model):
        aa_tw_model = load_model('models/AA_TW')
    if((sa * eng * rd == 1) and not sa_rd_model):
        sa_rd_model = load_model('models/SA_RD')
    if((aa * eng * rd == 1) and not aa_rd_model):
        aa_rd_model = load_model('models/AA_RD')
    if((sa * esp == 1) and not sa_esp_model):
        sa_esp_model = load_model('models/SA_ESP')
    if((aa * esp == 1) and not aa_esp_model):
        aa_esp_model = load_model('models/AA_ESP')

# Method to process the text if it is in English.
def text_preprocessing_english(s):
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

# Method to process the text if it is in Spanish.
def text_preprocessing_spanish(s):
    
    try:
        s = unidecode.unidecode(s)
    except:
        print("Error processing text. Maybe the text is not in spanish.")
    s = s.lower()
    #Remove links
    s = re.sub(r"http\S+", "", s)
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

# Method that tokenizes data depending on the tokenizer passed by parameters. 
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

# Method that tokenizes data depending on the tokenizer passed by parameters. (Only for reddit)
def prepare_data_only_rd_eng(input_text, tokenizer):
    token = tokenizer.encode_plus(
        input_text,
        max_length=256, 
        truncation=True, 
        padding='max_length', 
        add_special_tokens=True,
        return_tensors='tf'
    )
    return {
        'input_ids': tf.cast(token.input_ids, tf.float64),
        'attention_mask': tf.cast(token.attention_mask, tf.float64)
    }  

# AUX: Method that returns the sentiment prediction of a tweet.
def return_predict_sa_tw(model, processed_data):
    prob = model.predict(processed_data)[0][0]
    classes = "Positive"
    if prob < 0.5:
        prob = prob + 0.5
        classes = "Negative"
    return classes, prob

# AUX: Method that returns the sentiment prediction of a a comments.
def return_predict_sa_rd(model, processed_data, classes):
    probs = model.predict(processed_data)[0]
    probs = np.delete(probs, 0)
    prob = probs[np.argmax(probs)] / (probs[0] + probs[1])
    return classes[np.argmax(probs)], prob

# AUX: Method that returns the prediction of a tokenized data.
def return_predict(model, processed_data, classes):
    probs = model.predict(processed_data)[0]
    return classes[np.argmax(probs)], probs[np.argmax(probs)]

# Method that returns the prediction of some data depending on whether it is sentiment or aggressiveness.
def predict_text(model,data, option):
    if option == 0:
        return return_predict(model, data, ["Positive", "Negative"])
    elif option == 1:
        return return_predict(model, data, ["No hate", "Hate"])
    elif option == 2:
         return return_predict_sa_tw(model, data)
    else:
        return return_predict_sa_rd(model, data, ["Positive", "Negative"])

# AUX: Method that loads a model according to the path that has been passed by parameters. 
def load_model(path):
    return tf.keras.models.load_model(path)

# Method that predict a text written in spanish
def predict_spanish(data,aa,sa):
    data = prepare_data(data, tokenizer_esp)
    if(aa * sa==1):
        classPredicted_sa, acc_sa =predict_text(sa_esp_model,data, 0)
        classPredicted_aa, acc_aa =predict_text(aa_esp_model,data, 1)
        return classPredicted_aa + ": " + str(round(acc_aa * 100,2)) + "%" + "\n" +classPredicted_sa + ": " + str(round(acc_sa * 100,2)) + "%"
    elif(aa==1):
        classPredicted, acc = predict_text(aa_esp_model,data, 1)
        return classPredicted + ": " + str(round(acc* 100,2)) + "%"
    else:
        classPredicted, acc = predict_text(sa_esp_model,data, 0)
        return classPredicted + ": " + str(round(acc* 100,2)) + "%"

# Method that predict a text written in english
def predict_english_tw(data, aa, sa):
    tw_data = prepare_data(data, tokenizer_eng)
    if(aa * sa==1):
        classPredicted_aa, acc_aa =predict_text(aa_tw_model,tw_data, 1)
        classPredicted_sa, acc_sa =predict_text(sa_tw_model,tw_data, 2)
        return classPredicted_aa + ": " + str(round(acc_aa * 100,2)) + "%" + "\n" +classPredicted_sa + ": " + str(round(acc_sa * 100,2)) + "%"
    elif(aa==1):
        classPredicted, acc = predict_text(aa_tw_model,tw_data, 1)
        return classPredicted + ": " + str(round(acc * 100,2)) + "%"
    else:
        classPredicted, acc = predict_text(sa_tw_model,tw_data, 2)
        return classPredicted + ": " + str(round(acc * 100,2)) + "%"

# Method that predict a text written in spanish (Only for reddit)
def predict_english_rd(data, aa, sa):
    rd_data = prepare_data_only_rd_eng(data, tokenizer_eng)
    if(aa * sa==1):
        classPredicted_aa, acc_aa =predict_text(aa_rd_model,rd_data, 1)
        classPredicted_sa, acc_sa =predict_text(sa_rd_model,rd_data, 3)
        return classPredicted_aa + ": " + str(round(acc_aa * 100, 2)) + "%" + "\n" +classPredicted_sa + ": " + str(round(acc_sa * 100, 2)) + "%"
    elif(aa==1):
        classPredicted, acc = predict_text(aa_rd_model,rd_data, 1)
        return classPredicted + ": " + str(round(acc * 100, 2)) + "%"
    else:
        classPredicted, acc = predict_text(sa_rd_model,rd_data, 3)
        return classPredicted + ": " + str(round(acc * 100,2)) + "%"

# Method that predict a text
def predict(sa, aa, lang, sm, data):
    if(lang == 1):
        data = text_preprocessing_english(data)
        if(sm == 0):
            return predict_english_tw(data, aa, sa)
        else:
            return predict_english_rd(data, aa, sa)
    else:
        data = text_preprocessing_spanish(data)
        return predict_spanish(data,aa,sa)
    