from websocket_handshake import realizar_handshake
from mascaras import desmascarar_dados, mascarar_dados
from routes import process_request
import socket

def check_if_the_other_server_is_online(port):
    try:
        if port == 8080:
            return False
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect(('localhost', 8080))
        server_socket.close()
        return True
    except ConnectionRefusedError:
        return False
    except Exception as e:
        return False
    

def handle_client_connection(client_socket, port):
    try:
        print(client_socket)        
        if not realizar_handshake(client_socket):
            return  # Encerra a função se o handshake falhar
        # Loop para receber mensagens do cliente e responder
        while True:
            dados_recebidos = client_socket.recv(1024*2)
            if not dados_recebidos:
                break  # Encerra o loop se a conexão for fechada

            # Primeiro byte: FIN e opcode
            fin = dados_recebidos[0] >> 7
            opcode = dados_recebidos[0] & 0x0f

            # Segundo byte: MASK e Payload length
            mask = dados_recebidos[1] >> 7
            payload_length = dados_recebidos[1] & 0x7f

            if opcode == 0x8:
                break
            elif opcode == 0x1:
                # Mensagem de texto
                if mask == 1:
                    mascara = dados_recebidos[2:6]
                    payload = dados_recebidos[6:6+payload_length]
                    dados_desmascarados = desmascarar_dados(mascara, payload)
                    mensagem = dados_desmascarados.decode('utf-8')
                else:
                    print("Mensagem recebida sem máscara.")
            elif opcode == 0x2:
                print("Mensagem binária recebida, tratamento necessário.")
            else:
                print("Opcode não suportado recebido.")
            
            mensagem = mensagem.split(" ") # type: ignore
            if check_if_the_other_server_is_online(port):
                raise Exception("The other server is online.")
            if port == 8080:
                print('eai', mensagem)
            response = process_request(mensagem[0], mensagem[1:])
            response_masked = mascarar_dados(response)
            client_socket.send(response_masked)
    except Exception as e:
        e
    finally:
        client_socket.close()
