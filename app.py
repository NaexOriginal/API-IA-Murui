from flask import Flask, request, jsonify
from modelo_traduccion import initialize_model, translate_text  # Importa las funciones para inicializar el modelo y traducir

app = Flask(__name__)

# Inicializar el modelo al iniciar la aplicación
initialize_model()

@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    sentence = data.get('sentence')
    
    if not sentence:
        return jsonify({'error': 'No se proporcionó texto para traducir.'}), 400

    # Llama a la función de traducción con el modelo cargado
    translated_text = translate_text(sentence)

    return jsonify({'translated_text': translated_text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
