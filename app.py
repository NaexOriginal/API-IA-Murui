import socket
import json
from modelo_traduccion import translate_text

def handle_client_connection(client_socket):
    try:
        request = client_socket.recv(4096).decode('utf-8')

        headers, body = request.split('\r\n\r\n', 1)

        data = json.loads(body)
        sentence = data.get('sentence')
        model_filename = data.get('modelo')
        pkl_filename = data.get('pkl')

        if not sentence:
            response = json.dumps({'error': 'No se proporcionó texto para traducir.'})
            client_socket.sendall(f"HTTP/1.1 400 Bad Request\r\nContent-Type: application/json\r\nContent-Length: {len(response)}\r\n\r\n{response}".encode('utf-8'))
        elif not model_filename:
            response = json.dumps({'error': 'No se proporcionó el nombre del modelo.'})
            client_socket.sendall(f"HTTP/1.1 400 Bad Request\r\nContent-Type: application/json\r\nContent-Length: {len(response)}\r\n\r\n{response}".encode('utf-8'))
        elif not pkl_filename:
            response = json.dumps({'error': 'No se proporcionó el nombre del archivo .pkl.'})
            client_socket.sendall(f"HTTP/1.1 400 Bad Request\r\nContent-Type: application/json\r\nContent-Length: {len(response)}\r\n\r\n{response}".encode('utf-8'))
        else:
            translated_text = translate_text(sentence, model_filename, pkl_filename)
            response = json.dumps(translated_text)
            client_socket.sendall(f"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: {len(response)}\r\n\r\n{response}".encode('utf-8'))
    except Exception as e:
        response = json.dumps({'error': f'Error: {str(e)}'})
        client_socket.sendall(f"HTTP/1.1 500 Internal Server Error\r\nContent-Type: application/json\r\nContent-Length: {len(response)}\r\n\r\n{response}".encode('utf-8'))
    finally:
        client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5000))
    server.listen(5)
    print("Servidor escuchando en puerto 5000...")

    while True:
        client_socket, addr = server.accept()
        print(f"Conexión aceptada de {addr}")
        handle_client_connection(client_socket)

if __name__ == '__main__':
    start_server()