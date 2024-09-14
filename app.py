from flask import Flask, request, jsonify
from flask_cors import CORS
from modelo_traduccion import translate_text  # Importa la función para traducir

app = Flask(__name__)

CORS(app)

@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    sentence = data.get('sentence')
    model_filename = data.get('modelo')
    pkl_filename = data.get('pkl')

    if not sentence:
        return jsonify({'error': 'No se proporcionó texto para traducir.'}), 400
    if not model_filename:
        return jsonify({'error': 'No se proporcionó el nombre del modelo.'}), 400
    if not pkl_filename:
        return jsonify({'error': 'No se proporcionó el nombre del archivo .pkl.'}), 400

    # Llama a la función de traducción con el modelo y el dataset especificado
    translated_text = translate_text(sentence, model_filename, pkl_filename)
    print(translated_text)

    return jsonify(translated_text)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
