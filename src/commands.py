# commands.py is responsible for handling the database operations
from infra import Session
import models
from fastapi import HTTPException, status
from typing import Optional, List

def create_user(username: str, password: str) -> models.User:
    # Create a new User object
    user = models.User(username=username, password=password)
    
    # Using a context manager to handle the session
    with Session() as session:
        try:
            session.add(user)
            session.commit()
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    return user

def login_user(username: str, password: str) -> Optional[models.User]:
    # Using a context manager to handle the session
    with Session() as session:
        try:
            user = session.query(models.User).filter_by(username=username, password=password).first()
            if not user:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password.")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    return user

def add_friend(username: str, friend: str) -> models.Connection:
    # Using a context manager to handle the session
    with Session() as session:
        try:
            if username == friend:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot add yourself as a friend.")
            user = session.query(models.User).filter_by(username=username).first()
            friend = session.query(models.User).filter_by(username=friend).first()
            
            # Check if the user and friend exist
            if not user or not friend:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User or friend not found.")
            
            # Create a new Connection object
            connection = models.Connection(user=user, friend=friend)
            connection2 = models.Connection(user=friend, friend=user)
            
            session.add(connection)
            session.add(connection2)
            session.commit()
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    return connection

def send_message(sender_username: str, receiver_username: str, content: str) -> models.Message:
    # Usando um gerenciador de contexto para manipular a sessão
    with Session() as session:
        try:
            # Verifica se o remetente existe
            sender = session.query(models.User).filter_by(username=sender_username).first()
            if not sender:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Sender with username {sender_username} does not exist.")
            
            # Verifica se o destinatário existe
            receiver = session.query(models.User).filter_by(username=receiver_username).first()
            if not receiver:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Receiver with username {receiver_username} does not exist.")

            # Cria a mensagem
            message = models.Message(
                sender=sender,
                receiver=receiver,
                content=content,
            )

            # Adiciona e confirma a nova mensagem
            session.add(message)
            session.commit()
            session.refresh(message)

            return message

        except Exception as e:
            session.rollback()
            raise e

def get_all_users_and_msgs_friend_of_username(username: str, timestamp: str) -> dict:
    # Using a context manager to handle the session
    with Session() as session:
        try:
            user = session.query(models.User).filter_by(username=username).first()
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
            
            friends = [connection.friend for connection in user.connections]
            messages = session.query(models.Message).filter(
                (models.Message.sender_id == user.id) | (models.Message.receiver_id == user.id)  & (models.Message.timestamp > timestamp)
            ).all()

            # Prepare the result dictionary
            result = {}
            for friend in friends:
                friend_messages = [
                    {
                        "sender": message.sender.username,
                        "timestamp": message.timestamp.isoformat(),
                        "message": message.content
                    }
                    for message in messages
                    if message.receiver_id == friend.id or message.sender_id == friend.id
                ]
                result[friend.username] = friend_messages
        

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    return result