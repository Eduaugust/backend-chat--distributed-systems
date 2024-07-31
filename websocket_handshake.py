import base64
import hashlib

def realizar_handshake(client_socket):
    request = client_socket.recv(4096).decode('utf-8')  # Aumento do tamanho do buffer
    if 'Sec-WebSocket-Key: ' in request:
        key = (request.split('Sec-WebSocket-Key: ')[1]).split('\r\n')[0]
        accept_key = base64.b64encode(hashlib.sha1((key + '258EAFA5-E914-47DA-95CA-C5AB0DC85B11').encode('utf-8')).digest()).decode('utf-8')
        response = 'HTTP/1.1 101 Switching Protocols\r\n' \
                   'Upgrade: websocket\r\n' \
                   'Connection: Upgrade\r\n' \
                   'Sec-WebSocket-Accept: ' + accept_key + '\r\n\r\n'
        client_socket.send(response.encode('utf-8'))
        return True
    else:
        client_socket.close()
        return False