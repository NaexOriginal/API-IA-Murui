import numpy as np
from keras_transformer import get_model, decode
import pickle
import os

# Función para cargar el dataset
def cargar_dataset(pkl_filename):
    with open(pkl_filename, 'rb') as pkl_file:
        dataset = pickle.load(pkl_file)
    return dataset

# Función para crear diccionarios de tokens
def build_token_dict(token_list):
    token_dict = {'<pad>': 0, '<start>': 1, '<end>': 2}
    for tokens in token_list:
        for token in tokens:
            if token not in token_dict:
                token_dict[token] = len(token_dict)
    return token_dict

# Función para inicializar y cargar el modelo y los datos
def initialize_model(pkl_filename):
    dataset = cargar_dataset(pkl_filename)
    source_tokens = [sentence.split(' ') for sentence in dataset['texto']]
    target_tokens = [sentence.split(' ') for sentence in dataset['traduccion']]

    source_token_dict = build_token_dict(source_tokens)
    target_token_dict = build_token_dict(target_tokens)
    target_token_dict_inv = {v: k for k, v in target_token_dict.items()}

    source_max_len = max(map(len, source_tokens))

    model = get_model(
        token_num=max(len(source_token_dict), len(target_token_dict)),
        embed_dim=32,
        encoder_num=2,
        decoder_num=2,
        head_num=4,
        hidden_dim=128,
        dropout_rate=0.05,
        use_same_embed=False,
    )
    model.compile('adam', 'sparse_categorical_crossentropy')

    return model, source_token_dict, target_token_dict, target_token_dict_inv, source_max_len

# Función de traducción utilizando el modelo cargado
def translate_text(sentence, model_filename, pkl_filename):
    model, source_token_dict, target_token_dict, target_token_dict_inv, source_max_len = initialize_model(pkl_filename)
    
    model.load_weights(model_filename)
    
    sentence_tokens = [sentence.split(' ')]
    sentence_tokens = [['<start>'] + tokens + ['<end>'] + ['<pad>'] * (source_max_len - len(tokens) - 2) for tokens in sentence_tokens]
    tr_input = [list(map(lambda x: source_token_dict.get(x, 0), tokens)) for tokens in sentence_tokens][0]
    decoded = decode(
        model,
        tr_input,
        start_token=target_token_dict['<start>'],
        end_token=target_token_dict['<end>'],
        pad_token=target_token_dict['<pad>']
    )
    translated_text = ' '.join(map(lambda x: target_token_dict_inv.get(x, ''), decoded[1:-1]))
    return {
        "translated_text": translated_text, 
        "modelo": model_filename,
    }
