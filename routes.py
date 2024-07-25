# routes.py is responsible for processing the requests and calling the controllers to handle the business logic
from datetime import datetime, timedelta
import controllers
from typing import List

def process_request(endpoint: str, message: List[str]) -> bytes:
    if endpoint == "/":
        return b"Hello World"
    elif endpoint == "/sendMessage":
        if not message or len(message) < 3:
            return b"Numero de argumentos invalido"
        return controllers.send_message(sender=message[0], receiver=message[1], content=" ".join(message[2:]))
    elif endpoint == "/register":
        if len(message) != 2:
            return b"Numero de argumentos invalido"
        return controllers.register(username=message[0], password=message[1])
    elif endpoint == "/login":
        if len(message) != 2:
            return b"Numero de argumentos invalido"
        return controllers.login(username=message[0], password=message[1])
    elif endpoint == "/addFriend":
        if len(message) != 2:
            return b"Numero de argumentos invalido"
        return controllers.add_friend(username=message[0], friend=message[1])
    elif endpoint == "/getAll":
        if len(message) != 1:
            return b"Numero de argumentos invalido"
        timestamp = message[1] if len(message) == 2 else (datetime.now() - timedelta(days=365.25*10)).isoformat()
        return controllers.get_all(username=message[0], timestamp=timestamp)
    else:
        return b"Endpoint nao encontrado"
