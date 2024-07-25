# controllers.py is responsible for handling the business logic of the application
import commands
from datetime import datetime

def get_current_timestamp() -> str:
    """Retorna o timestamp atual no formato ISO 8601."""
    return datetime.now().isoformat()

def register(username: str, password: str) -> bytes:
    try:
        commands.create_user(username, password)
        dict_messages = {'status': 'success', 'data': 'Usuário registrado com sucesso.', 'timestamp': get_current_timestamp()}
        return bytes(str(dict_messages), 'utf-8')
    except Exception as e:
        dict_messages = {'status': 'error', 'data': 'Falha ao registrar usuário.', 'timestamp': get_current_timestamp()}
        return bytes(str(dict_messages), 'utf-8')

def login(username: str, password: str) -> bytes:
    try:
        user = commands.login_user(username, password)
        if user:
            dict_messages = {'status': 'success', 'data': 'Usuário logado com sucesso.', 'timestamp': get_current_timestamp()}
            return bytes(str(dict_messages), 'utf-8')
        else:
            dict_messages = {'status': 'error', 'data': 'Nome de usuário ou senha inválidos.', 'timestamp': get_current_timestamp()}
            return bytes(str(dict_messages), 'utf-8')
    except Exception as e:
        dict_messages = {'status': 'error', 'data': 'Falha ao fazer login do usuário.', 'timestamp': get_current_timestamp()}
        return bytes(str(dict_messages), 'utf-8')

def add_friend(username: str, friend: str) -> bytes:
    try:
        commands.add_friend(username, friend)
        dict_messages = {'status': 'success', 'data': 'Amigo adicionado com sucesso.', 'timestamp': get_current_timestamp()}
        return bytes(str(dict_messages), 'utf-8')
    except Exception as e:
        dict_messages = {'status': 'error', 'data': 'Falha ao adicionar amigo.', 'timestamp': get_current_timestamp()}
        return bytes(str(dict_messages), 'utf-8')

def send_message(sender: str, receiver: str, content: str) -> bytes:
    try:
        commands.send_message(sender, receiver, content)
        dict_messages = {'status': 'success', 'data': 'Mensagem enviada com sucesso.', 'timestamp': get_current_timestamp()}
        return bytes(str(dict_messages), 'utf-8')
    except Exception as e:
        dict_messages = {'status': 'error', 'data': 'Falha ao enviar mensagem.', 'timestamp': get_current_timestamp()}
        return bytes(str(dict_messages), 'utf-8')

def get_all(username: str, timestamp: str) -> bytes:
    try:
        dict_messages = commands.get_all_users_and_msgs_friend_of_username(username, timestamp)
        response = {'status': 'success', 'data': dict_messages, 'timestamp': get_current_timestamp()}
        return bytes(str(response), 'utf-8')
    except Exception as e:
        dict_messages = {'status': 'error', 'data': 'Falha ao recuperar todas as mensagens.', 'timestamp': get_current_timestamp()}
        return bytes(str(dict_messages), 'utf-8')
